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

    def __str__(self) -> str:
        """
        Creates a string representation of the object.

        :return: object string representation.
        """
        object_string = "["
        counter = 0
        dict_size = len(self.__dict__.items())
        for key, value in self.__dict__.items():
            object_string += f'{key}: {value}'
            if counter != (dict_size - 1):
                object_string += ", "
            counter += 1
        object_string += "]"
        return object_string


class LuxerOneClient:
    """
    Unofficial LuxerOne Python client.

    :param username: Optional username. If one is not provided, :meth:`LuxerOneClient.login` must be called
                         manually or a token must be provided.
    :param password: The password associated with the provided username.
    :param auth_token_details: Optional parameter. If no username or password is provided, an existing token can
                               be provided.
    """
    def __init__(self, username: str = None, password: str = None,
                 auth_token_details: AuthTokenDetails = None):
        """
        :param username: Optional username. If one is not provided, :meth:`LuxerOneClient.login` must be called
                         manually or a token must be provided.
        :param password: The password associated with the provided username.
        :param auth_token_details: Optional parameter. If no username or password is provided, an existing token can
                                   be provided.
        :raise LuxerOneAPIException: when failure to login occurs.
        """
        self._auth_token_details = None
        if username is not None and password is not None:
            self.login(username, password)
            return
        if auth_token_details is not None:
            self._auth_token_details = auth_token_details

    def login(self, username: str, password: str, ttl: int = 300) -> None:
        """
        Gets an API auth token to submit requests.

        :param username: Username
        :param password: Password
        :param ttl: Time to live for the token in seconds. Defaults to 300 (five minutes) with a max of 1800
                    (thirty minutes).
        :raise LuxerOneAPIException: when failure to login occurs.
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
        self._auth_token_details = AuthTokenDetails(login_resp["token"], ttl)

    def get_long_lived_token(self, ttl: int = 18000000) -> AuthTokenDetails:
        """
        Gets a long-lived API auth token. Must have received an auth token prior to making this call by either
        supplying your own or providing your login credentials to the class constructor or by calling
        :meth:`LuxerOneClient.login`.

        **Please note** that there appears to be a bug with the server-side logout functionality, resulting in
        :meth:`LuxerOneClient.logout` having no affect. It is not advised to create long-lived tokens as there
        is no way to invalidate them until Luxer One fixes this issue.

        One the request for the long-lived token has been processed, the token used by the client will be automatically
        be changed to use the new token and the prior auth token will be invalidated.

        :param ttl: time to live in seconds for the long-lived token. Max value is 18000000 (208.3 days)
        :raise RequestNotAuthenticatedException: when called without having an auth token set.
        :raise TokenExpiredException: when an expired auth token is used.
        :raise LuxerOneAPIException: when the API call fails unexpectedly.
        :returns: the auth token details for the long-lived-token.
        """
        self._validate_token()
        data = {
            "as": "token",
            "expire": ttl,
        }
        login_resp = api_request(API.auth_long_term, token=self._auth_token_details.token, data=data)
        # invalidate the prior token
        self.logout()
        self._auth_token_details = AuthTokenDetails(login_resp["token"], ttl)
        return self._auth_token_details

    def get_pending_packages(self) -> list[Package]:
        """
        Gets the list of current packages that have been delivered but not picked up.

        :raise RequestNotAuthenticatedException: when called without having an auth token set.
        :raise TokenExpiredException: when an expired auth token is used.
        :raise LuxerOneAPIException: when the API call fails unexpectedly.
        :returns: a list of packages that are pending pickup
        """
        self._validate_token()
        response = api_request(API.pending_packages, token=self._auth_token_details.token)
        packages = list()
        for pacakge_data in response:
            packages.append(Package(package_data=pacakge_data))
        return packages

    def get_user_info(self) -> UserInfo:
        """
        Returns a UserInfo object containing the information for the authenticated user.

        :raise RequestNotAuthenticatedException: when called without having an auth token set.
        :raise TokenExpiredException: when an expired auth token is used.
        :raise LuxerOneAPIException: when the API call fails unexpectedly.
        :returns: User Information.
        """
        self._validate_token()
        response = api_request(API.user_info, token=self._auth_token_details.token)
        return UserInfo(response)

    def get_package_history(self) -> list[HistoricalPackage]:
        """
        Gets a history of all packages received includes pending packages. Seems to be limited to last 50.

        :raise RequestNotAuthenticatedException: when called without having an auth token set.
        :raise TokenExpiredException: when an expired auth token is used.
        :raise LuxerOneAPIException: when the API call fails unexpectedly.
        :returns: a list of the last 50 packages.
        """
        self._validate_token()
        response = api_request(API.package_history, token=self._auth_token_details.token)
        packages = list()
        for pacakge_data in response:
            packages.append(HistoricalPackage(package_data=pacakge_data))
        return packages

    def logout(self) -> Union[dict, None]:
        """
        Logout from the LuxerOne API. This will invalidate (in theory) the auth token that is being used by the client,
        so be careful when calling this method if you are using a long-lived token. Testing has shown that calling
        logout does not appear to invalidate the token.

        :raise RequestNotAuthenticatedException: when called without having an auth token set.
        :raise LuxerOneAPIException: when the API call fails unexpectedly.
        :return: logout response or None if the token is already expired.
        """
        if self._auth_token_details is None:
            raise RequestNotAuthenticatedException("You have not received an API Auth token yet, login to get one.")
        if not self._auth_token_details.is_expired():
            data = {
                "revoke": self._auth_token_details,
            }
            response = api_request(API.logout, token=self._auth_token_details.token, data=data)
            return response
        return None

    def set_setting(self, key, value) -> dict:
        """
        Changes user settings. Keys are values from :meth:`LuxerOneClient.get_user_info`
        Not all options are changeable.

        This is still a work in progress and will eventually provide wrapper classes
        for manipulating user information.

        :raise RequestNotAuthenticatedException: when called without having an auth token set.
        :raise TokenExpiredException: when an expired auth token is used.
        :raise LuxerOneAPIException: when the API call fails unexpectedly.
        :return: the api response.
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
        response = api_request(API.update_user_setting, token=self._auth_token_details.token, data=data)
        return response

    def _set_auth_token_details(self, auth_token_details: AuthTokenDetails) -> None:
        """
        Sets the AuthTokenDetails to be used by the client. Intended to be used for unit testing only.

        :param auth_token_details: Details to set.
        """

    def _validate_token(self):
        """
        Validates the auth token, ensuring it is not expired.
        """
        if self._auth_token_details is None:
            raise RequestNotAuthenticatedException("You have not received an API Auth token yet, login to get one.")
        if self._auth_token_details.is_expired():
            raise TokenExpiredException("Your API Auth token expired, please login again. to receive a new one.")
