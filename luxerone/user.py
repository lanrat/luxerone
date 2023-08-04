"""
Wrapper classes for all information relating to the user.
"""


class UserInfoLocation:
    """
    Delivery location information associated with a user.
    """

    class Location:
        """
        Location information.
        """

        def __init__(self, location_info: dict):
            """
            :param location_info:
            """
            self.id = None
            self.name = None
            self.lockerLocation = None
            self.timezone = None
            self.holdPackages = None
            self.holdPackagesLimit = None
            for element in self.__dict__.keys():
                try:
                    self.__dict__[element] = location_info[element]
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

    class LocationUser:
        """
        Class representing the Location of a user for the UserInfo object.
        """

        def __init__(self, location_user_info: dict):
            """
            :param location_user_info:
            """
            self.id = None
            self.user_id = None
            self.location_id = None
            self.modified = None
            self.active = None
            self.is_house_account = None
            self.externalId = None
            self.created = None
            self.optOutReason = None
            self.signupFeeExempt = None
            self.deliveriesFeeExempt = None
            self.notMarkAsPickedUp = None
            self.alwaysMoveToLocker = None
            self.doNotMarkAllAsPickedUp = None
            self.welcomeEmailSent = None
            self.boxAccessCode = None
            self.customers_imports_id = None
            self.importer_correlation_id = None
            for element in self.__dict__.keys():
                try:
                    self.__dict__[element] = location_user_info[element]
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

    def __init__(self, all_locations_data: dict):
        """
        :param all_locations_data:
        """
        self.location = UserInfoLocation.Location(all_locations_data["Location"])
        self.location_user = UserInfoLocation.LocationUser(all_locations_data["LocationsUser"])

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


class UserInfo:
    """
    Class representing the user information.
    """

    def __init__(self, user_info: dict):
        """
        :param user_info:
        """
        self.id = None
        self.firstName = None
        self.lastName = None
        self.email = None
        self.phone = None
        self.secondaryEmail = None
        self.allowEmails = None
        self.allowSms = None
        self.smsOption = None
        self.allowPushNotifications = None
        self.lowLocker = None
        self.vacationsFrom = None
        self.vacationsTo = None
        self.termsAccepted = None
        self.requiresCreditCard = None
        self.hasValidCreditCard = None
        self.foodDeliveryEnabled = None
        self.foodDeliveryImageUrl = None
        self.foodDeliveryDestinationUrl = None
        self.bannerImageUrl = None
        self.bannerDestinationUrl = None
        self.peerToPeerDeliveryEnabled = None
        self.lockerLocation = None
        self.showLockerLocation = None
        self.showRatingPrompt = None
        for element in self.__dict__.keys():
            try:
                self.__dict__[element] = user_info[element]
            except KeyError:
                self.__dict__[element] = None

        self.all_locations = list()
        try:
            locations = user_info["allLocations"]
            for location in locations:
                self.all_locations.append(UserInfoLocation(location))
        except KeyError:
            pass

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
