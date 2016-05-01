from inputs.weight import Weight
from inputs.temperature import Temperature
from status_helpers import TeapotStatus
from server_communicator import ServerCommunicator

weight_sensor = Weight()
temperature_sensor = Temperature()
server_link = ServerCommunicator()
teapot_status = TeapotStatus()
last_status = None
last_number_of_cups = None


def do_work():
    server_link.send_queued_update_if_time()
    global last_status, last_number_of_cups

    current_weight = weight_sensor.get_reading()
    temperature = temperature_sensor.get_reading()
    is_rising = temperature_sensor.is_rising()

    status = teapot_status.get_teapot_status(
        current_weight, temperature, is_rising)

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
