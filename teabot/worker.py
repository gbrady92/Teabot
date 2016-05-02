from teabot.inputs.weight import Weight
from teabot.inputs.temperature import Temperature
from teabot.status_helpers import TeapotStatus
from teabot.server_communicator import ServerCommunicator

weight_sensor = Weight()
temperature_sensor = Temperature()
server_link = ServerCommunicator()
teapot_status = TeapotStatus()
last_status = None
last_number_of_cups = None


def do_work():
    """This is the entry point for teabot, this function polls the sensors for
    their lastest readings and then updates the state machine based on them.

    If the state of the teapot changes or the number of cups remaining changes
    this information is posted to the server where it is stored for analytics
    and querying purposes.
    """
    server_link.send_queued_update_if_time()
    global last_status, last_number_of_cups

    current_weight = weight_sensor.get_reading()
    temperature = temperature_sensor.get_reading()
    temperature_is_rising_or_constant = \
        temperature_sensor.is_rising_or_constant()

    status = teapot_status.get_teapot_status(
        current_weight, temperature, temperature_is_rising_or_constant)

    if status.teapot_state != last_status or \
            status.number_of_cups_remaining != last_number_of_cups:
        ServerCommunicator.send_update(
            status.teapot_state,
            status.timestamp,
            status.number_of_cups_remaining
        )
        last_status = status.teapot_state
        last_number_of_cups = status.number_of_cups_remaining


if __name__ == "main":
    while True:
        do_work()
