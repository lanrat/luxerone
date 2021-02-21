import urllib.request, urllib.parse
import json
import uuid

API_BASE = "https://resident-api.luxerone.com/resident_api/v1"

default_headers = {
    "content-type": "application/x-www-form-urlencoded",
    "accept": "application/json, text/plain, */*",
    "User-Agent": "okhttp/3.12.1",
}

def gen_uuid():
    """ returns a 64 but uuid as a hex string for new clients """
    id = uuid.uuid4().int & (1<<64)-1
    return hex(id)[2:]


def api_request(url, method="GET", token=None, data=None):
    """ helper function for calling api endpoints

    token:  the API token to add to the authorization header
    data:   the message body for POST request that will be URL encoded

    returns the "data" field of the response or None on error
    """
    if data:
        data = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(url, method=method, data=data, headers=default_headers)
    if token:
        req.add_header("authorization", "LuxerOneApi " + token)

    # parsing response
    r = urllib.request.urlopen(req).read()
    resp = json.loads(r.decode('utf-8'))
    return resp


def login(username, password):
    """ login to the service, returns a longterm token for later API calls """
    url = API_BASE + "/auth/login"
    id = gen_uuid()
    data = {
        "as": "token",
        "expires": 1800,
        "remember": True,
        "uuid": id,
        "username": username,
        "password": password,
    }
    login_resp = api_request(url, method="POST", data=data)

    if "error" in login_resp:
        raise Exception("login error: %s" % login_resp["error"])

    # longterm login
    url = API_BASE + "/auth/longterm"
    data = {
        "as": "token",
        "expire": 18000000,
    }
    longterm_resp = api_request(url, method="POST", data=data, token=login_resp["data"]["token"])

    if "error" in longterm_resp:
        raise Exception("longterm login error: %s" % longterm_resp["error"])

    return longterm_resp["data"]["token"]


def pending(token):
    """ returns a list of packages that are pending pickup """
    url = API_BASE + "/deliveries/pendings"
    resp = api_request(url, token=token)

    if "error" in resp:
        raise Exception("pending error: %s" % resp["error"])

    return resp["data"]


def user_info(token):
    """ returns a dictionary of user info
    keys from user info can be used in set_setting() to toggle settings
    """
    url = API_BASE + "/user/info"
    resp = api_request(url, token=token)

    if "error" in resp:
        raise Exception("user_info error: %s" % resp["error"])

    return resp["data"]


def history(token):
    """ returns a history of all packages received
    includes pending packages
    """
    url = API_BASE + "/deliveries/history"
    resp = api_request(url, token=token)

    if "error" in resp:
        raise Exception("history error: %s" % resp["error"])

    return resp["data"]

def logout(token):
    """ logout from the LuxerOne API
    this function call appears to have no affect, likely broken server side
    """
    url = API_BASE + "/auth/logout"
    data = {
        "revoke": token,
    }
    resp = api_request(url, token=token, data=data, method="POST")

    if "error" in resp:
        raise Exception("logout error: %s" % resp["error"])

    return resp["data"]

def set_setting(token, key, value):
    """ changes user settings.
    keys are values from user_info()
    not all options are changeable
    """
    url = API_BASE + "/user/settings"
    # true/false are represented as 1/0
    if value == True:
        value = 1
    if value == False:
        value = 0
    data = {
        key: value,
    }
    resp = api_request(url, token=token, data=data, method="POST")

    if "error" in resp:
        raise Exception("set_setting error: %s" % resp["error"])


    return resp["data"]


def print_package(data):
    """ print some package information """
    print("%s\t%s\t%s\t%s\t%s" % (data['id'], data['delivered'][:-6],data['carrier'],data['lockerNumber'],data['accessCode']))

def print_packages(data, limit=0):
    """ print a list of packages """
    if limit != 0:
        data = data[:limit]
    for p in data:
        print_package(p)
