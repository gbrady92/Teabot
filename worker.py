from __future__ import division
from inputs.weight import Weight
from inputs.temperature import Temperature
from status_helpers import get_teapot_status

weight_sensor = Weight()
temperature_sensor = Temperature()

cup_of_tea_weight = 250

def get_cups_remaining(current_teapot_weight):
	return int(current_teapot_weight / cup_of_tea_weight)


while True:
    weight = weight_sensor.get_reading()
    temperature = temperature_sensor.get_reading()
    status = get_teapot_status(
        weight=weight, temperature=temperature,
        new_teapot_weight=3042, empty_teapot_weight=1472,
        cold_teapot_temperature=40, temperature_rising=temperature_sensor.is_rising())
    print status
    print get_cups_remaining(weight)
