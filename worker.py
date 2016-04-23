from inputs.weight import Weight
from inputs.temperature import Temperature
from status_helpers import get_teapot_status

weight_sensor = Weight()
temperature_sensor = Temperature()

#TODO Get readings from db.
weight_of_tea_in_cup = 250
empty_teapot_weight = 1472

while True:
    weight = weight_sensor.get_reading()
    temperature = temperature_sensor.get_reading()
    status = get_teapot_status(
        weight=weight, temperature=temperature,
        new_teapot_weight=3042, empty_teapot_weight=1472,
        cold_teapot_temperature=40, temperature_rising=temperature_sensor.is_rising(), weight_of_tea_in_cup=weight_of_tea_in_cup)