from inputs.weight import Weight
from inputs.temperature import Temperature
from status_helpers import get_teapot_status

weight_sensor = Weight()
temperature_sensor = Temperature()

#TODO Get readings from db.
tea_in_cup_weight = 250
empty_teapot_weight = 1472

def get_cups_remaining(teapot_weight):
	return int((teapot_weight - empty_teapot_weight) / tea_in_cup_weight)


while True:
    weight = weight_sensor.get_reading()
    temperature = temperature_sensor.get_reading()
    status = get_teapot_status(
        weight=weight, temperature=temperature,
        new_teapot_weight=3042, empty_teapot_weight=1472,
        cold_teapot_temperature=40, temperature_rising=temperature_sensor.is_rising())
    print status
    print get_cups_remaining(weight)