"""
Client for interacting with the LuxerOne Residential API
"""
import datetime
from typing import Union

from luxerone._api_utils import API, gen_uuid, api_request
from luxerone.package import Package, HistoricalPackage
from luxerone.user import UserInfo
from luxerone.exceptions import RequestNotAuthenticatedException, TokenExpiredException


class AuthTokenDetails:
    """
    Contains token details and utilities to check if the token has expired.
    """
    def __init__(self, token: str, ttl: int):
        """
        :param token: auth token.
        :param ttl: time to live in seconds.
        """
        self.token = token
        self.expires_at = datetime.timedelta(seconds=ttl) + datetime.datetime.now()

    def is_expired(self) -> bool:
        """
        Whether the token has expired.

        :return: true if expired, else false.
        """
        return datetime.datetime.now() > self.expires_at


class LuxerOneClient:
    """
    Unofficial LuxerOne Python client.
    """
    def __init__(self, username: str = None, password: str = None):
        """
        :param username: optional username. If one is not provided, :meth:`login<client.LuxerOneClient.login>` must be
                         called manually.
        :param password: optional password. If one is not provided, login must be called manually.
        """
        self.auth_token_details = None
        if username is not None and password is not None:
            self.login(username, password)

    def login(self, username: str, password: str, ttl: int = 1800) -> None:
        """
        Gets an API auth token to submit requests.

        :param username: username
        :param password: password
        :param ttl: time to live for the token in seconds. Defaults to the max of 1800 (thirty minutes).
        """
        generated_id = gen_uuid()
        data = {
            "as": "token",
            "expires": ttl,
            "remember": True,
            "uuid": generated_id,
            "username": username,
            "password": password,
        }
        login_resp = api_request(api=API.auth, data=data)
        self.auth_token_details = AuthTokenDetails(login_resp["token"], ttl)

    def get_long_lived_token(self, ttl: int = 18000000) -> None:
        """
        Gets a long-lived API auth token. Must have already :meth:`logged in<client.LuxerOneClient.login>` to request
        the token.

        :param ttl: time to live in seconds for the long-lived token. Max value is 18000000 (208.3 days)
        """
        self._validate_token()
        data = {
            "as": "token",
            "expire": ttl,
        }
        login_resp = api_request(API.auth_long_term, data=data)
        self.auth_token_details = AuthTokenDetails(login_resp["token"], ttl)

    def get_pending_packages(self) -> list:
        """
        Gets the list of current packages that have been delivered but not picked up.

        :returns: a list of packages that are pending pickup
        """
        self._validate_token()
        response = api_request(API.pending_packages, token=self.auth_token_details.token)
        packages = list()
        for pacakge_data in response:
            packages.append(Package(package_data=pacakge_data))
        return packages

    def get_user_info(self) -> UserInfo:
        """
        Returns a UserInfo object containing the information for the authenticated user.

        :returns: User Information.
        """
        self._validate_token()
        response = api_request(API.user_info, token=self.auth_token_details.token)
        return UserInfo(response)

    def get_package_history(self) -> list[HistoricalPackage]:
        """
        Gets a history of all packages received includes pending packages. Seems to be limited to last 50.

        :returns: list last 50 packages
        """
        self._validate_token()
        response = api_request(API.package_history, token=self.auth_token_details.token)
        packages = list()
        for pacakge_data in response:
            packages.append(HistoricalPackage(package_data=pacakge_data))
        return packages

    def logout(self) -> Union[dict, None]:
        """
        Logout from the LuxerOne API.

        :return: logout response or None if the token is already expired.
        """
        if not self.auth_token_details.is_expired():
            data = {
                "revoke": self.auth_token_details,
            }
            response = api_request(API.logout, token=self.auth_token_details.token, data=data)
            return response
        return None

    def set_setting(self, key, value):
        """
        changes user settings.
        keys are values from user_info()
        not all options are changeable
        :return:
        """
        self._validate_token()
        # TODO figure out which settings can be set and create a class for it
        # true/false are represented as 1/0
        if value:
            value = 1
        else:
            value = 0
        data = {
            key: value,
        }
        response = api_request(API.update_user_setting, token=self.auth_token_details.token, data=data)
        return response

    def _validate_token(self):
        """
        Validates the auth token, ensuring it is not expired.
        """
        if self.auth_token_details is None:
            raise RequestNotAuthenticatedException("You have not received an API Auth token yet, login to get one.")
        if self.auth_token_details.is_expired():
            raise TokenExpiredException("Your API Auth token expired, please login again. to receive a new one.")
