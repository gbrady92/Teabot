from fysom import Fysom
from teabot.constants import (
    NO_TEAPOT, FULL_TEAPOT, GOOD_TEAPOT, COLD_TEAPOT, EMPTY_TEAPOT,
)

# Cached teapot_state_machine, retrive it using get_teapot_state_machine
teapot_state_machine = None


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
                'name': 'temp_below_cold_weight_above_empty',
                'src': NO_TEAPOT,
                'dst': COLD_TEAPOT
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
                'name': 'temp_below_cold_weight_above_empty',
                'src': FULL_TEAPOT,
                'dst': COLD_TEAPOT
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
                'dst': COLD_TEAPOT
            },
            {
                'name': 'temp_rising_weight_above_full',
                'src': COLD_TEAPOT,
                'dst': FULL_TEAPOT
            },
            {
                'name': 'weight_below_empty',
                'src': COLD_TEAPOT,
                'dst': EMPTY_TEAPOT
            },
            {
                'name': 'scales_empty',
                'src': COLD_TEAPOT,
                'dst': COLD_TEAPOT
            },
            {
                'name': 'temp_below_cold_weight_above_empty',
                'src': COLD_TEAPOT,
                'dst': COLD_TEAPOT
            },
            {
                'name': 'weight_above_empty_below_full',
                'src': COLD_TEAPOT,
                'dst': COLD_TEAPOT
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
        ]
    })
    return fsm


def get_teapot_state_machine():
    """Returns a single instance of the teapot finite state machine"""
    global teapot_state_machine
    if not teapot_state_machine:
        teapot_state_machine = generate_teapot_state_machine()
    return teapot_state_machine
