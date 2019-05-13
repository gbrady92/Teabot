from os import environ
from datetime import timedelta

NO_TEAPOT = "NO_TEAPOT"
FULL_TEAPOT = "FULL_TEAPOT"
GOOD_TEAPOT = "GOOD_TEAPOT"
EMPTY_TEAPOT = "EMPTY_TEAPOT"

# Number of minutes we want to wait before reporting a new teapot to the
# endpoint. By default we assume that a teapot takes 5 minutes to brew.
BREW_DELAY_MINUTES = 5
# How many cups are in a full pot of tea?
CUPS_IN_A_FULL_TEAPOT = 4
# Weight of an empty teapot. This was naively calculated by putting the teapot
# on the scales and seeing what the scales reported it as (then adding 100g
# as the weight does fluctuate over time).
EMPTY_TEAPOT_WEIGHT = 1550
# Used to determine when a new teapot has been created. We assume that if the
# weight on the scales has gone up and the last teapot was created over 40
# minutes ago it is a new teapot.
NEW_TEAPOT_REFRESH_PERIOD = timedelta(minutes=40)
# How many grams in a teacup-cup if a teacup could gram grams?
WEIGHT_OF_TEA_IN_CUP = 280
# Nought.
ZERO_WEIGHT = 0

ENDPOINT_BASE_URL = environ.get("TEABOT_BASE_URL", "https://teabot.co.uk/")


class TeapotStatuses(object):
    """Defines the states the teapot can be in"""

    """We have only seen empty scales since we started, so we have no info."""
    NO_TEAPOT = NO_TEAPOT
    """Transitioning to this state causes a POST to /teaReady in 5 mins."""
    FULL_TEAPOT = FULL_TEAPOT
    """A teapot that we don't want to notify about."""
    GOOD_TEAPOT = GOOD_TEAPOT
    """A pot with no tea in.
    Note that if the scales are empty, we try to keep the state as it was, but
    it's entirely possible that it might slip into this state?
    """
    EMPTY_TEAPOT = EMPTY_TEAPOT


class Constants(object):
    """Defines environmental constants that influence the state of the
    teapot
    """
    def get_empty_teapot_weight(self):
        return EMPTY_TEAPOT_WEIGHT

    def get_weight_of_tea_in_cup(self):
        return WEIGHT_OF_TEA_IN_CUP

    def get_zero_weight(self):
        return ZERO_WEIGHT

    def get_brew_delay_minutes(self):
        return BREW_DELAY_MINUTES

    def get_endpoint_base_url(self):
        return ENDPOINT_BASE_URL

    def get_lower_bound_for_full_teapot(self):
        return EMPTY_TEAPOT_WEIGHT + (
            WEIGHT_OF_TEA_IN_CUP * CUPS_IN_A_FULL_TEAPOT
        )

    def get_new_teapot_refresh_period(self):
        return NEW_TEAPOT_REFRESH_PERIOD
