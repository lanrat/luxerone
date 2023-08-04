import json
import urllib.parse
import urllib.request
import uuid

_API_BASE = "https://resident-api.luxerone.com/resident_api/v1"
_DEFAULT_HEADERS = {
    "content-type": "application/x-www-form-urlencoded",
    "accept": "application/json, text/plain, */*",
    "User-Agent": "okhttp/3.12.1",
}


def _gen_uuid() -> str:
    """
    Generates a UUID.
    :return: a 64 bit uuid as a hex string for new clients
    """
    generated_id = uuid.uuid4().int & (1 << 64) - 1
    return hex(generated_id)[2:]


def _api_request(url, method="GET", token=None, data=None):
    """
    Helper function for calling api endpoints
    :param token:  the API token to add to the authorization header
    :param data:   the message body for POST request that will be URL encoded
    :return: the returned json parsed as a dict
    """
    if data:
        data = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(url, method=method, data=data, headers=_DEFAULT_HEADERS)
    if token:
        req.add_header("authorization", "LuxerOneApi " + token)

    # parsing response
    r = urllib.request.urlopen(req).read()
    resp = json.loads(r.decode('utf-8'))
    return resp


class Locker:
    def __init__(self, package_data: dict):
        """
        Locker information class.
        :param package_data: package data in json format from the API.
        """
        self.lockerId = None
        self.lockerNumber = None
        self.lockerTypeId = None
        self.lockerType = None
        for element in self.__dict__.keys():
            try:
                self.__dict__[element] = package_data[element]
            except KeyError:
                self.__dict__[element] = None

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


class Carrier:
    def __init__(self, package_data: dict):
        """
        Carrier information class.
        :param package_data: package data in json format from the API.
        """
        self.carrier = None
        self.carrierLogo = None
        self.trackingNumber = None
        for element in self.__dict__.keys():
            try:
                self.__dict__[element] = package_data[element]
            except KeyError:
                self.__dict__[element] = None

    def __str__(self):
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


class Location:
    def __init__(self, package_data: dict):
        """
        Locker information class.
        :param package_data: package data in json format from the API.
        """
        self.location = None
        self.locationId = None
        self.locationAddress = None
        self.lockerLocation = None
        self.timezoneOffset = None
        for element in self.__dict__.keys():
            try:
                self.__dict__[element] = package_data[element]
            except KeyError:
                self.__dict__[element] = None

    def __str__(self):
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


class Package:
    def __init__(self, package_data: dict):
        """
        Package information class.
        :param package_data: package data in json format from the API.
        """
        self.id = None
        self.deliveryTypeId = None
        self.delivered = None
        self.pickedup = None
        self.holdUntil = None
        self.accessCode = None
        self.isPerishable = False
        self.status = None
        self.charge = None
        self.pickupToken = None
        self.labels = None
        for element in self.__dict__.keys():
            try:
                self.__dict__[element] = package_data[element]
            except KeyError:
                self.__dict__[element] = None
        self.carrier = Carrier(package_data)
        self.locker = Locker(package_data)
        self.location = Location(package_data)

    def __str__(self):
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


class HistoricalPackage(Package):
    def __init__(self, package_data: dict):
        """
        Historical Package info class.
        :param package_data: package data in json format from the API.
        """
        super().__init__(package_data)
        try:
            self.resident = package_data["resident"]
        except KeyError:
            self.resident = None
        try:
            self.signature = package_data["signature"]
        except KeyError:
            self.signature = None

    def __str__(self):
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
    def __init__(self):
        """
        Unofficial LuxerOne Python client.
        """
        self._token = None

    def login(self, username: str, password: str) -> None:
        """

        :param username:
        :param password:
        :return:
        """
        url = _API_BASE + "/auth/login"
        generated_id = _gen_uuid()
        data = {
            "as": "token",
            "expires": 1800,
            "remember": True,
            "uuid": generated_id,
            "username": username,
            "password": password,
        }
        login_resp = _api_request(url, method="POST", data=data)

        if "error" in login_resp:
            raise Exception("login error: %s" % login_resp["error"])

        # longterm login
        url = _API_BASE + "/auth/longterm"
        data = {
            "as": "token",
            "expire": 18000000,
        }
        longterm_resp = _api_request(url, method="POST", data=data, token=login_resp["data"]["token"])

        if "error" in longterm_resp:
            raise Exception("longterm login error: %s" % longterm_resp["error"])

        self._token = longterm_resp["data"]["token"]

    def get_pending_packages(self):
        """
        Gets the list of current packages that have been delivered but not picked up.
        :returns: a list of packages that are pending pickup
        """
        url = _API_BASE + "/deliveries/pendings"
        resp = _api_request(url, token=self._token)

        if "error" in resp:
            raise Exception("pending error: %s" % resp["error"])
        # TODO return pacakge objects
        return resp["data"]

    def get_user_info(self):
        """
        returns a dictionary of user info
        keys from user info can be used in set_setting() to toggle settings
        """
        # TODO make a user info object
        url = _API_BASE + "/user/info"
        resp = _api_request(url, token=self._token)

        if "error" in resp:
            raise Exception("user_info error: %s" % resp["error"])

        return resp["data"]

    def get_package_history(self):
        """ returns a history of all packages received
        includes pending packages
        seems to be limited to last 50
        """
        url = _API_BASE + "/deliveries/history"
        resp = _api_request(url, token=self._token)

        if "error" in resp:
            raise Exception("history error: %s" % resp["error"])

        # TODO return historical package objects
        return resp["data"]

    def logout(self):
        """ logout from the LuxerOne API
        this function call appears to have no affect, likely broken server side
        """
        url = _API_BASE + "/auth/logout"
        data = {
            "revoke": self._token,
        }
        resp = _api_request(url, token=self._token, data=data, method="POST")

        if "error" in resp:
            raise Exception("logout error: %s" % resp["error"])

        return resp["data"]

    def set_setting(self, key, value):
        """
        changes user settings.
        keys are values from user_info()
        not all options are changeable
        """
        # TODO figure out which settings can be set and create an object for it
        url = _API_BASE + "/user/settings"
        # true/false are represented as 1/0
        if value:
            value = 1
        else:
            value = 0
        data = {
            key: value,
        }
        resp = _api_request(url, token=self._token, data=data, method="POST")

        if "error" in resp:
            raise Exception("set_setting error: %s" % resp["error"])

        return resp["data"]
