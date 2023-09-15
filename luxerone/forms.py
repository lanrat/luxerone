"""
Request Data models.
"""
import uuid


def _gen_uuid() -> str:
    """
    Generates a UUID.
    :return: a 64 bit uuid as a hex string for new clients
    """
    generated_id = uuid.uuid4().int & (1 << 64) - 1
    return hex(generated_id)[2:]


class _RequestForm:
    def get_data(self) -> dict[str, any]:
        """
        Gets the data as a dictionary ready for an API request.

        :return: form data as dict
        """
        return self.__dict__


class _LoginRequestForm(_RequestForm):
    """
    Login request form.

    :param username: username
    :param password: password
    :param ttl: token time to live in seconds
    """

    def __init__(self, username: str, password: str, ttl: int):
        """
        :param username: username
        :param password: password
        :param ttl: token time to live in seconds
        """
        self.username = username
        self.password = password
        self.expires = ttl
        self.uuid = _gen_uuid()
        self.remember = True

    def get_data(self) -> dict[str, any]:
        """
        Gets the data as a dictionary ready for an API request.

        :return: form data as dict
        """
        data = dict()
        data["as"] = "token"
        for key in self.__dict__.keys():
            data[key] = self.__dict__[key]
        return data


class _LongLivedTokenForm(_RequestForm):
    """
    Long-lived token request form.

    :param ttl: token time to live in seconds.
    """

    def __init__(self, ttl: int):
        """
        :param ttl: token time to live in seconds.
        """
        self.ttl = ttl

    def get_data(self) -> dict[str, any]:
        """
        Gets the data as a dictionary ready for an API request.

        :return: form data as dict
        """
        data = dict()
        data["expires"] = self.ttl
        data["as"] = "token"
        return data


class _LogoutForm(_RequestForm):
    """
    Logout request form.

    :param token: token to expire
    """

    def __init__(self, token: str):
        """
        :param token: token to expire
        """
        self.revoke = token


class _ResetPasswordForm(_RequestForm):
    """
    Reset password request form.

    :param email: email of the account to reset the password for.
    """

    def __init__(self, email: str):
        """
        :param email: email of the account to reset the password for.
        """
        self.email = email


class UpdateUserSettingsForm(_RequestForm):
    def __init__(self, first_name: str = None,
                 last_name: str = None,
                 email: str = None,
                 phone: str = None,
                 secondary_email: str = None,
                 allow_emails: bool = None,
                 allow_sms: bool = None,
                 allow_push_notifications: bool = None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.secondaryEmail = secondary_email
        self.allowEmails = allow_emails
        self.allowSms = allow_sms
        self.allowPushNotifications = allow_push_notifications

    def get_data(self) -> dict[str, any]:
        data = dict()
        for key in self.__dict__.keys():
            if self.__dict__[key] is not None:
                data[key] = self.__dict__[key]
        return data
