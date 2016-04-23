from collections import namedtuple
from datetime import datetime


def get_descriptor(tea_status):
    status = namedtuple("status", ["tea_state", "timestamp"])
    return status(tea_state=tea_status, timestamp=datetime.now())


def get_teapot_status(
        temperature, weight, new_teapot_temperature, new_teapot_weight,
        empty_teapot_weight, cold_teapot_temperature):

    if temperature > new_teapot_temperature and weight > new_teapot_weight:
        return get_descriptor("NEW_TEAPOT")
    if weight > empty_teapot_weight and weight < new_teapot_weight:
        if temperature > cold_teapot_temperature:
            return get_descriptor("GOOD_POT")
        else:
            return get_descriptor("COLD_POT_WITH_TEA")
    if weight < empty_teapot_weight:
        return get_descriptor("EMPTY_TEAPOT")
    return get_descriptor("ERROR_STATE")
