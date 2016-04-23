from collections import namedtuple
from datetime import datetime
import logging
logging.basicConfig(level=logging.DEBUG)


def get_descriptor(tea_status, num_of_cups):
    status = namedtuple("status", ["tea_state", "timestamp", "num_of_cups"])
    return status(tea_state=tea_status, timestamp=datetime.now(), num_of_cups)


def get_is_teapot_full(new_teapot_weight, teapot_weight, weight_of_tea_in_cup):
    lower_bound = new_teapot_weight - weight_of_tea_in_cup
    return lower_bound <= teapot_weight

def get_remaining_cups(teapot_weight, empty_teapot_weight, weight_of_tea_in_cup):
  remaining_cups = (teapot_weight - empty_teapot_weight) / weight_of_tea_in_cup
  if remaining_cups >= 0.70:
    return 1
  else:
    return int(remaining_cups)

def get_teapot_status(
         current_weight, temperature, new_teapot_weight,
        empty_teapot_weight, cold_teapot_temperature, temperature_rising, weight_of_tea_in_cup):

    logging.debug("\nTemperature %s\
                   \nWeight %s\
                   \nNew Teapot Weight %s\
                   \nEmpty Teapot Weight %s\
                   \nCold Teapot Temp %s\
                   \nTemperature Rising %s"
                   % (temperature, weight, new_teapot_weight,
                   empty_teapot_weight,
                   cold_teapot_temperature, temperature_rising)
                 )
    num_of_cups = get_remaining_cups(current_weight, empty_teapot_weight, weight_of_tea_in_cup)

    if temperature_rising and get_is_teapot_full(
            new_teapot_weight, weight, 250):
        return get_descriptor("NEW_TEAPOT", num_of_cups)
    if weight > empty_teapot_weight and weight < new_teapot_weight:
        if temperature > cold_teapot_temperature:
            return get_descriptor("GOOD_POT", num_of_cups)
        else:
            return get_descriptor("COLD_POT_WITH_TEA", num_of_cups)
    if weight < empty_teapot_weight:
        return get_descriptor("EMPTY_TEAPOT", num_of_cups)
    return get_descriptor("ERROR_STATE")
