from collections import namedtuple
from datetime import datetime, timedelta
import logging

from constants import TeapotStatuses
logging.basicConfig(level=logging.DEBUG)

new_teapot_time = None
teapot_status = None


def get_descriptor(tea_status, num_of_cups):
    status = namedtuple("status", ["tea_state", "timestamp", "num_of_cups"])
    return status(
        tea_state=tea_status, timestamp=datetime.now(), num_cups=num_of_cups)


def get_is_teapot_full(
        weight_of_tea_in_new_pot, tea_weight, weight_of_tea_in_cup):
    lower_bound = weight_of_tea_in_new_pot - weight_of_tea_in_cup
    return lower_bound <= tea_weight


def get_remaining_cups(
        teapot_weight, empty_teapot_weight, weight_of_tea_in_cup):
    remaining_cups = \
        (teapot_weight - empty_teapot_weight) / weight_of_tea_in_cup
    if remaining_cups >= 0.70:
        return 1
    else:
        return int(remaining_cups)

def get_teapot_brewed_status(current_new_teapot_time):
    global new_teapot_time
    if new_teapot_time is None:
        new_teapot_time = new_teapot_time
        return TeapotStatuses.NEW_TEAPOT
    elif new_teapot_time + timedelta(minutes=5) <= datetime.now():
            return TeapotStatuses.NEW_TEAPOT
    new_teapot_time = None
    return TeapotStatuses.BREWED_TEAPOT


def get_teapot_status(
        current_weight, temperature, new_teapot_weight,
        empty_teapot_weight, cold_teapot_temperature, temperature_rising,
        weight_of_tea_in_cup):
    global teapot_status

    logging.debug("\nTemperature %s\
                   \nWeight %s\
                   \nNew Teapot Weight %s\
                   \nEmpty Teapot Weight %s\
                   \nCold Teapot Temp %s\
                   \nTemperature Rising %s"
                   % (temperature, current_weight, new_teapot_weight,
                   empty_teapot_weight,
                   cold_teapot_temperature, temperature_rising)
    )
    num_of_cups = get_remaining_cups(
        current_weight, empty_teapot_weight, weight_of_tea_in_cup)

    if temperature_rising and get_is_teapot_full(
            new_teapot_weight - empty_teapot_weight,
            current_weight - empty_teapot_weight,
            weight_of_tea_in_cup):
        # Only evaluated if NEW_TEAPOT criteria is met.
        if teapot_status == TeapotStatuses.BREWED_TEAPOT:
            teapot_status = TeapotStatuses.OLD_BREWED_TEAPOT
        else:
            teapot_status = get_teapot_brewed_status(datetime.now())

        return get_descriptor(teapot_status, num_of_cups)

    if current_weight > empty_teapot_weight and \
            current_weight < new_teapot_weight:
        if temperature > cold_teapot_temperature:
            teapot_status = TeapotStatuses.GOOD_TEAPOT
            return get_descriptor(teapot_status, num_of_cups)
        else:
            return get_descriptor(TeapotStatuses.COLD_TEAPOT, num_of_cups)

    if current_weight < empty_teapot_weight:
        teapot_status = TeapotStatuses.NO_TEAPOT
        return get_descriptor(teapot_status, num_of_cups)

    if num_of_cups == 0:
        teapot_status = TeapotStatuses.EMPTY_TEAPOT
        return get_descriptor(teapot_status, num_of_cups)

    return get_descriptor(TeapotStatuses.ERROR_STATE)
