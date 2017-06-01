from fysom import Fysom
from teabot.constants import TeapotStatuses

# Cached teapot_state_machine, retrive it using get_teapot_state_machine
teapot_state_machine = None


def generate_teapot_state_machine():
    """Generates the teapot finite state machine defining all of the states
    and valid transitions between them.

    Returns
        - Fysom - finite state machine
    """
    fsm = Fysom({
        'initial': TeapotStatuses.NO_TEAPOT,
        'events': [
            {
                'name': 'temp_rising_weight_above_full',
                'src': TeapotStatuses.NO_TEAPOT,
                'dst': TeapotStatuses.FULL_TEAPOT
            },
            {
                'name': 'scales_empty',
                'src': TeapotStatuses.NO_TEAPOT,
                'dst': TeapotStatuses.NO_TEAPOT
            },
            {
                'name': 'weight_below_empty',
                'src': TeapotStatuses.NO_TEAPOT,
                'dst': TeapotStatuses.EMPTY_TEAPOT
            },
            {
                'name': 'temp_below_cold_weight_above_empty',
                'src': TeapotStatuses.NO_TEAPOT,
                'dst': TeapotStatuses.COLD_TEAPOT
            },
            {
                'name': 'weight_above_empty_below_full',
                'src': TeapotStatuses.NO_TEAPOT,
                'dst': TeapotStatuses.GOOD_TEAPOT
            },
            {
                'name': 'weight_below_empty',
                'src': TeapotStatuses.FULL_TEAPOT,
                'dst': TeapotStatuses.EMPTY_TEAPOT
            },
            {
                'name': 'weight_above_empty_below_full',
                'src': TeapotStatuses.FULL_TEAPOT,
                'dst': TeapotStatuses.GOOD_TEAPOT
            },
            {
                'name': 'temp_below_cold_weight_above_empty',
                'src': TeapotStatuses.FULL_TEAPOT,
                'dst': TeapotStatuses.COLD_TEAPOT
            },
            {
                'name': 'scales_empty',
                'src': TeapotStatuses.FULL_TEAPOT,
                'dst': TeapotStatuses.FULL_TEAPOT
            },
            {
                'name': 'temp_rising_weight_above_full',
                'src': TeapotStatuses.FULL_TEAPOT,
                'dst': TeapotStatuses.FULL_TEAPOT
            },
            {
                'name': 'weight_below_empty',
                'src': TeapotStatuses.GOOD_TEAPOT,
                'dst': TeapotStatuses.EMPTY_TEAPOT
            },
            {
                'name': 'weight_above_empty_below_full',
                'src': TeapotStatuses.GOOD_TEAPOT,
                'dst': TeapotStatuses.GOOD_TEAPOT
            },
            {
                'name': 'temp_rising_weight_above_full',
                'src': TeapotStatuses.GOOD_TEAPOT,
                'dst': TeapotStatuses.FULL_TEAPOT
            },
            {
                'name': 'scales_empty',
                'src': TeapotStatuses.GOOD_TEAPOT,
                'dst': TeapotStatuses.GOOD_TEAPOT
            },
            {
                'name': 'temp_below_cold_weight_above_empty',
                'src': TeapotStatuses.GOOD_TEAPOT,
                'dst': TeapotStatuses.COLD_TEAPOT
            },
            {
                'name': 'temp_rising_weight_above_full',
                'src': TeapotStatuses.COLD_TEAPOT,
                'dst': TeapotStatuses.FULL_TEAPOT
            },
            {
                'name': 'weight_below_empty',
                'src': TeapotStatuses.COLD_TEAPOT,
                'dst': TeapotStatuses.EMPTY_TEAPOT
            },
            {
                'name': 'scales_empty',
                'src': TeapotStatuses.COLD_TEAPOT,
                'dst': TeapotStatuses.COLD_TEAPOT
            },
            {
                'name': 'temp_below_cold_weight_above_empty',
                'src': TeapotStatuses.COLD_TEAPOT,
                'dst': TeapotStatuses.COLD_TEAPOT
            },
            {
                'name': 'weight_above_empty_below_full',
                'src': TeapotStatuses.COLD_TEAPOT,
                'dst': TeapotStatuses.COLD_TEAPOT
            },
            {
                'name': 'temp_rising_weight_above_full',
                'src': TeapotStatuses.EMPTY_TEAPOT,
                'dst': TeapotStatuses.FULL_TEAPOT
            },
            {
                'name': 'weight_below_empty',
                'src': TeapotStatuses.EMPTY_TEAPOT,
                'dst': TeapotStatuses.EMPTY_TEAPOT
            },
            {
                'name': 'scales_empty',
                'src': TeapotStatuses.EMPTY_TEAPOT,
                'dst': TeapotStatuses.EMPTY_TEAPOT
            },
            {
                'name': 'weight_above_empty_below_full',
                'src': TeapotStatuses.EMPTY_TEAPOT,
                'dst': TeapotStatuses.GOOD_TEAPOT
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
