"""
Utilities for interacting with the Luxer One REST API.
"""
import enum
import json
import urllib.parse
import urllib.request

from luxerone.exceptions import LuxerOneAPIException
from luxerone.forms import _RequestForm
_API_BASE = "https://resident-api.luxerone.com/resident_api/v1"
_DEFAULT_HEADERS = {
    "content-type": "application/x-www-form-urlencoded",
    "accept": "application/json, text/plain, */*",
    "User-Agent": "okhttp/3.12.1",
}


class _APIDefinition:
    def __init__(self, endpoint: str, method: str):
        self.endpoint = endpoint
        self.method = method


class API(enum.Enum):
    # auth
    auth = _APIDefinition("/auth/login", "POST")
    reset_password = _APIDefinition("/auth/resetpassword", "POST")
    auth_long_term = _APIDefinition("/auth/longterm", "POST")
    logout = _APIDefinition("/auth/logout", "POST")
    # packages
    pending_packages = _APIDefinition("/deliveries/pendings", "GET")
    package_history = _APIDefinition("/deliveries/history", "GET")
    # user info/settings
    user_info = _APIDefinition("/user/info", "GET")
    update_user_setting = _APIDefinition("/user/settings", "POST")

    def get_endpoint(self) -> str:
        """
        Gets the endpoint associated with the API call
        :return: the endpoint.
        """
        return self.value.endpoint

    def get_method(self) -> str:
        """
        Gets the HTTP method used for the API call.
        :return: the HTTP method
        """
        return self.value.method


class LuxerOneApiResponse:
    def __init__(self, api_response):
        """
        Class representing an API response.
        :param api_response: raw api response from url_open.
        """
        decoded_response = json.loads(api_response.decode('utf-8'))
        self.data = None
        self.error = None
        for element in self.__dict__.keys():
            try:
                self.__dict__[element] = decoded_response[element]
            except KeyError:
                self.__dict__[element] = None

    def has_error(self) -> bool:
        """
        Determines whether the response contains an error field.
        :return: whether the response contains an error.
        """
        return self.error is not None

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


def api_request(api: API, token: str = None, form: _RequestForm = None) -> dict[any, any]:
    """
    Helper function for calling api endpoints
    :param api:
    :param token:  the API token to add to the authorization header
    :param form:   the message body for POST request that will be URL encoded
    :return: the returned json parsed as a dict
    """
    url = _API_BASE + api.get_endpoint()
    data = None
    if form:
        data = urllib.parse.urlencode(form.get_data()).encode()
    req = urllib.request.Request(url, method=api.get_method(), data=data, headers=_DEFAULT_HEADERS)
    if token:
        req.add_header("authorization", "LuxerOneApi " + token)

    # parsing response
    raw_response = urllib.request.urlopen(req)
    response = LuxerOneApiResponse(raw_response.read())
    raw_response.close()
    if response.has_error():
        raise LuxerOneAPIException(f'Received an error response from the API: {response.error}')
    return response.data
