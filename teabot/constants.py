from os import environ
from datetime import timedelta


class TeapotStatuses(object):
    """Defines the states the teapot can be in"""

    GOOD_TEAPOT = "GOOD_TEAPOT"
    COLD_TEAPOT = "COLD_TEAPOT"
    NO_TEAPOT = "NO_TEAPOT"
    EMPTY_TEAPOT = "EMPTY_TEAPOT"
    FULL_TEAPOT = "FULL_TEAPOT"


class Constants(object):
    """Defines environmental constants that influence the state of the
    teapot
    """

    def __init__(self):
        self.FULL_TEAPOT_WEIGHT = None
        self.EMPTY_TEAPOT_WEIGHT = None
        self.COLD_TEAPOT_TEMPERATURE = None
        self.WEIGHT_OF_TEA_IN_CUP = None
        self.ZERO_WEIGHT = None
        self.BREW_DELAY_MINUTES = None
        self.ENDPOINT_BASE_URL = None
        self.NEW_TEAPOT_REFRESH_PERIOD = None

    def get_full_teapot_weight(self):
        if not self.FULL_TEAPOT_WEIGHT:
            # TODO Replace with actual database lookup
            self.FULL_TEAPOT_WEIGHT = 796
        return self.FULL_TEAPOT_WEIGHT

    def get_empty_teapot_weight(self):
        if not self.EMPTY_TEAPOT_WEIGHT:
            # TODO Replace with actual database lookup
            self.EMPTY_TEAPOT_WEIGHT = 58
        return self.EMPTY_TEAPOT_WEIGHT

    def get_cold_teapot_temperature(self):
        if not self.COLD_TEAPOT_TEMPERATURE:
            # TODO Replace with actual database lookup
            self.COLD_TEAPOT_TEMPERATURE = 20
        return self.COLD_TEAPOT_TEMPERATURE

    def get_weight_of_tea_in_cup(self):
        if not self.WEIGHT_OF_TEA_IN_CUP:
            # TODO Replace with actual database lookup
            self.WEIGHT_OF_TEA_IN_CUP = 280
        return self.WEIGHT_OF_TEA_IN_CUP

    def get_zero_weight(self):
        if not self.ZERO_WEIGHT:
            # TODO Replace with actual database lookup
            self.ZERO_WEIGHT = 0
        return self.ZERO_WEIGHT

    def get_brew_delay_minutes(self):
        if not self.BREW_DELAY_MINUTES:
            # TODO Replace with actual database lookup
            self.BREW_DELAY_MINUTES = 5
        return self.BREW_DELAY_MINUTES

    def get_endpoint_base_url(self):
        if not self.ENDPOINT_BASE_URL:
            self.ENDPOINT_BASE_URL = environ.get(
                "TEABOT_BASE_URL", "https://teabot.co.uk/")
        return self.ENDPOINT_BASE_URL

    def get_weight_of_tea_in_full_teapot(self):
        return self.get_full_teapot_weight() - self.get_empty_teapot_weight()

    def get_lower_bound_for_full_teapot(self):
        return self.get_weight_of_tea_in_full_teapot() - \
            (self.get_weight_of_tea_in_cup() / 2)

    def get_new_teapot_refresh_period(self):
        if not self.NEW_TEAPOT_REFRESH_PERIOD:
            # TODO Replace with actual database lookup
            self.NEW_TEAPOT_REFRESH_PERIOD = timedelta(minutes=40)
        return self.NEW_TEAPOT_REFRESH_PERIOD
