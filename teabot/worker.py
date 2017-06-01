import sys

import rollbar

from teabot.status_helpers import TeapotStatus


if '--fake' in sys.argv:
    from teabot.inputs.fake import FakeSensor
    weight_sensor = FakeSensor(key='weight', pipe=sys.stdin)
    temperature_sensor = FakeSensor(key='temperature', pipe=sys.stdin)
else:
    from teabot.inputs.weight import Weight
    from teabot.inputs.temperature import Temperature
    weight_sensor = Weight()
    temperature_sensor = Temperature()


teapot_status = TeapotStatus()
rollbar.init("")


def do_work():
    """This is the entry point for teabot, this function polls the sensors for
    their lastest readings and then updates the state machine based on them.

    If the state of the teapot changes or the number of cups remaining changes
    this information is posted to the server where it is stored for analytics
    and querying purposes.
    """
    current_weight = weight_sensor.read_and_store(wait=True)
    temperature = temperature_sensor.read_and_store(wait=True)
    temperature_is_rising_or_constant = \
        temperature_sensor.is_rising_or_constant()

    teapot_status.get_teapot_status(
        current_weight, temperature, temperature_is_rising_or_constant)


if __name__ == "__main__":
    while True:
        try:
            do_work()
        except Exception as e:
            rollbar.report_exc_info()
            raise
