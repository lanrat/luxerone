"""
Wrapper classes for all information relating to package deliveries.
"""


class Locker:
    """
    Locker information.
    """

    def __init__(self, package_data: dict):
        """
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
    """
    Carrier information.
    """

    def __init__(self, package_data: dict):
        """
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
    """
    Location information regarding the package delivery location.
    """

    def __init__(self, package_data: dict):
        """
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
    """
    Package information.
    """

    def __init__(self, package_data: dict):
        """
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
    """
    Historical Package information.
    """

    def __init__(self, package_data: dict):
        """
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
