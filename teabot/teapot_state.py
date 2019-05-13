from fysom import Fysom
from teabot.constants import (
    NO_TEAPOT, FULL_TEAPOT, GOOD_TEAPOT, EMPTY_TEAPOT,
)
from teabot.server_communicator import ServerCommunicator

# Cached teapot_state_machine, retrive it using get_teapot_state_machine
teapot_state_machine = None

last_number_of_cups = None
server_link = ServerCommunicator()


def handle_state_change_event(event):
    global last_number_of_cups

    if event.src == 'none':
        return True

    if event.number_of_cups_remaining <= 0 and event.dst != EMPTY_TEAPOT:
        return True

    server_link.send_queued_update_if_time()

    server_link.send_status_update(
        event.dst,
        event.timestamp,
        event.number_of_cups_remaining,
        event.weight
    )
    last_number_of_cups = event.number_of_cups_remaining
    return True


def handle_state_reenter_event(event):
    global last_number_of_cups

    if event.number_of_cups_remaining <= 0 and event.dst != EMPTY_TEAPOT:
        return True

    server_link.send_queued_update_if_time()

    if event.number_of_cups_remaining != last_number_of_cups:
        server_link.send_status_update(
            event.dst,
            event.timestamp,
            event.number_of_cups_remaining,
            event.weight
        )
    else:
        print "status hasn't changed"
    last_number_of_cups = event.number_of_cups_remaining
    return True


def generate_teapot_state_machine():
    """Generates the teapot finite state machine defining all of the states
    and valid transitions between them.

    Returns
        - Fysom - finite state machine
    """
    fsm = Fysom({
        'initial': NO_TEAPOT,
        'events': [
            {
                'name': 'temp_rising_weight_above_full',
                'src': NO_TEAPOT,
                'dst': FULL_TEAPOT
            },
            {
                'name': 'scales_empty',
                'src': NO_TEAPOT,
                'dst': NO_TEAPOT
            },
            {
                'name': 'weight_below_empty',
                'src': NO_TEAPOT,
                'dst': EMPTY_TEAPOT
            },
            {
                'name': 'weight_above_empty_below_full',
                'src': NO_TEAPOT,
                'dst': GOOD_TEAPOT
            },
            {
                'name': 'weight_below_empty',
                'src': FULL_TEAPOT,
                'dst': EMPTY_TEAPOT
            },
            {
                'name': 'weight_above_empty_below_full',
                'src': FULL_TEAPOT,
                'dst': GOOD_TEAPOT
            },
            {
                'name': 'scales_empty',
                'src': FULL_TEAPOT,
                'dst': FULL_TEAPOT
            },
            {
                'name': 'temp_rising_weight_above_full',
                'src': FULL_TEAPOT,
                'dst': FULL_TEAPOT
            },
            {
                'name': 'weight_below_empty',
                'src': GOOD_TEAPOT,
                'dst': EMPTY_TEAPOT
            },
            {
                'name': 'weight_above_empty_below_full',
                'src': GOOD_TEAPOT,
                'dst': GOOD_TEAPOT
            },
            {
                'name': 'temp_rising_weight_above_full',
                'src': GOOD_TEAPOT,
                'dst': FULL_TEAPOT
            },
            {
                'name': 'scales_empty',
                'src': GOOD_TEAPOT,
                'dst': GOOD_TEAPOT
            },
            {
                'name': 'temp_below_cold_weight_above_empty',
                'src': GOOD_TEAPOT,
                'dst': FULL_TEAPOT
            },
            {
                'name': 'temp_rising_weight_above_full',
                'src': EMPTY_TEAPOT,
                'dst': FULL_TEAPOT
            },
            {
                'name': 'weight_below_empty',
                'src': EMPTY_TEAPOT,
                'dst': EMPTY_TEAPOT
            },
            {
                'name': 'scales_empty',
                'src': EMPTY_TEAPOT,
                'dst': EMPTY_TEAPOT
            },
            {
                'name': 'weight_above_empty_below_full',
                'src': EMPTY_TEAPOT,
                'dst': GOOD_TEAPOT
            }
        ],
        'callbacks': {
            'onchangestate': handle_state_change_event,
            # FULL_TEAPOT should never be reentered but whatever
            'onreenterFULL_TEAPOT': handle_state_reenter_event,
            'onreenterGOOD_TEAPOT': handle_state_reenter_event,
            'onreenterEMPTY_TEAPOT': handle_state_reenter_event,
        }
    })
    return fsm


def get_teapot_state_machine():
    """Returns a single instance of the teapot finite state machine"""
    global teapot_state_machine
    if not teapot_state_machine:
        teapot_state_machine = generate_teapot_state_machine()
    return teapot_state_machine
