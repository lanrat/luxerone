import enum
import json
import urllib.parse
import urllib.request
import uuid

from luxerone.exceptions import LuxerOneAPIException

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
    auth = _APIDefinition("/auth/login", "POST")
    auth_long_term = _APIDefinition("/auth/longterm", "POST")
    logout = _APIDefinition("/auth/logout", "POST")
    pending_packages = _APIDefinition("/deliveries/pendings", "GET")
    package_history = _APIDefinition("/deliveries/history", "GET")
    user_info = _APIDefinition("/user/info", "GET")
    update_user_setting = _APIDefinition("/user/settings", "POST")

    def get_endpoint(self):
        """
        Gets the endpoint associated with the API call
        :return: the endpoint.
        """
        return self.value.endpoint

    def get_method(self):
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


def gen_uuid() -> str:
    """
    Generates a UUID.
    :return: a 64 bit uuid as a hex string for new clients
    """
    generated_id = uuid.uuid4().int & (1 << 64) - 1
    return hex(generated_id)[2:]


def api_request(api: API, token=None, data=None) -> dict:
    """
    Helper function for calling api endpoints
    :param api:
    :param token:  the API token to add to the authorization header
    :param data:   the message body for POST request that will be URL encoded
    :return: the returned json parsed as a dict
    """
    url = _API_BASE + api.get_endpoint()
    if data:
        data = urllib.parse.urlencode(data).encode()
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
