from inputs.weight import Weight
from inputs.temperature import Temperature
from status_helpers import get_teapot_status

weight_sensor = Weight()
temperature_sensor = Temperature()

while True:
    weight = weight_sensor.get_reading()
    temperature = temperature_sensor.get_reading()
    status = get_teapot_status(
        weight=weight, temperature=temperature, new_teapot_temperature=55,
        new_teapot_weight=3000, empty_teapot_weight=0,
        cold_teapot_temperature=20, temperature_rising=temperature_sensor.is_rising())
    print status
