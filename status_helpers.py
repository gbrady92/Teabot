from collections import namedtuple
from datetime import datetime
import logging

from constants import TeapotStatuses
logging.basicConfig(level=logging.DEBUG)


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


def get_teapot_status(
        current_weight, temperature, new_teapot_weight,
        empty_teapot_weight, cold_teapot_temperature, temperature_rising,
        weight_of_tea_in_cup):

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
        return get_descriptor(TeapotStatuses.NEW_TEAPOT, num_of_cups)
    if current_weight > empty_teapot_weight and \
            current_weight < new_teapot_weight:
        if temperature > cold_teapot_temperature:
            return get_descriptor(TeapotStatuses.GOOD_TEAPOT, num_of_cups)
        else:
            return get_descriptor(TeapotStatuses.COLD_TEAPOT, num_of_cups)
    if current_weight < empty_teapot_weight:
        return get_descriptor(TeapotStatuses.NO_TEAPOT, num_of_cups)
    if num_of_cups == 0:
        return get_descriptor(TeapotStatuses.EMPTY_TEAPOT, num_of_cups)
    return get_descriptor(TeapotStatuses.ERROR_STATE)
