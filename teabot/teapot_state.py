from fysom import Fysom
from teabot.constants import TeapotStatuses, Transistions

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
                'name': Transistions.TEMP_RISING_WEIGHT_ABOVE_FULL,
                'src': TeapotStatuses.NO_TEAPOT,
                'dst': TeapotStatuses.FULL_TEAPOT
            },
            {
                'name': Transistions.SCALES_EMPTY,
                'src': TeapotStatuses.NO_TEAPOT,
                'dst': TeapotStatuses.NO_TEAPOT
            },
            {
                'name': Transistions.WEIGHT_BELOW_EMPTY,
                'src': TeapotStatuses.NO_TEAPOT,
                'dst': TeapotStatuses.EMPTY_TEAPOT
            },
            {
                'name': Transistions.TEMP_BELOW_COLD_AND_WEIGHT_ABOVE_EMPTY,
                'src': TeapotStatuses.NO_TEAPOT,
                'dst': TeapotStatuses.COLD_TEAPOT
            },
            {
                'name': Transistions.WEIGHT_ABOVE_EMPTY_BELOW_FULL,
                'src': TeapotStatuses.NO_TEAPOT,
                'dst': TeapotStatuses.GOOD_TEAPOT
            },
            {
                'name': Transistions.WEIGHT_BELOW_EMPTY,
                'src': TeapotStatuses.FULL_TEAPOT,
                'dst': TeapotStatuses.EMPTY_TEAPOT
            },
            {
                'name': Transistions.WEIGHT_ABOVE_EMPTY_BELOW_FULL,
                'src': TeapotStatuses.FULL_TEAPOT,
                'dst': TeapotStatuses.GOOD_TEAPOT
            },
            {
                'name': Transistions.TEMP_BELOW_COLD_AND_WEIGHT_ABOVE_EMPTY,
                'src': TeapotStatuses.FULL_TEAPOT,
                'dst': TeapotStatuses.COLD_TEAPOT
            },
            {
                'name': Transistions.SCALES_EMPTY,
                'src': TeapotStatuses.FULL_TEAPOT,
                'dst': TeapotStatuses.FULL_TEAPOT
            },
            {
                'name': Transistions.TEMP_RISING_WEIGHT_ABOVE_FULL,
                'src': TeapotStatuses.FULL_TEAPOT,
                'dst': TeapotStatuses.FULL_TEAPOT
            },
            {
                'name': Transistions.WEIGHT_BELOW_EMPTY,
                'src': TeapotStatuses.GOOD_TEAPOT,
                'dst': TeapotStatuses.EMPTY_TEAPOT
            },
            {
                'name': Transistions.WEIGHT_ABOVE_EMPTY_BELOW_FULL,
                'src': TeapotStatuses.GOOD_TEAPOT,
                'dst': TeapotStatuses.GOOD_TEAPOT
            },
            {
                'name': Transistions.TEMP_RISING_WEIGHT_ABOVE_FULL,
                'src': TeapotStatuses.GOOD_TEAPOT,
                'dst': TeapotStatuses.FULL_TEAPOT
            },
            {
                'name': Transistions.SCALES_EMPTY,
                'src': TeapotStatuses.GOOD_TEAPOT,
                'dst': TeapotStatuses.GOOD_TEAPOT
            },
            {
                'name': Transistions.TEMP_BELOW_COLD_AND_WEIGHT_ABOVE_EMPTY,
                'src': TeapotStatuses.GOOD_TEAPOT,
                'dst': TeapotStatuses.COLD_TEAPOT
            },
            {
                'name': Transistions.TEMP_RISING_WEIGHT_ABOVE_FULL,
                'src': TeapotStatuses.COLD_TEAPOT,
                'dst': TeapotStatuses.FULL_TEAPOT
            },
            {
                'name': Transistions.WEIGHT_BELOW_EMPTY,
                'src': TeapotStatuses.COLD_TEAPOT,
                'dst': TeapotStatuses.EMPTY_TEAPOT
            },
            {
                'name': Transistions.SCALES_EMPTY,
                'src': TeapotStatuses.COLD_TEAPOT,
                'dst': TeapotStatuses.COLD_TEAPOT
            },
            {
                'name': Transistions.TEMP_BELOW_COLD_AND_WEIGHT_ABOVE_EMPTY,
                'src': TeapotStatuses.COLD_TEAPOT,
                'dst': TeapotStatuses.COLD_TEAPOT
            },
            {
                'name': Transistions.WEIGHT_ABOVE_EMPTY_BELOW_FULL,
                'src': TeapotStatuses.COLD_TEAPOT,
                'dst': TeapotStatuses.COLD_TEAPOT
            },
            {
                'name': Transistions.TEMP_RISING_WEIGHT_ABOVE_FULL,
                'src': TeapotStatuses.EMPTY_TEAPOT,
                'dst': TeapotStatuses.FULL_TEAPOT
            },
            {
                'name': Transistions.WEIGHT_BELOW_EMPTY,
                'src': TeapotStatuses.EMPTY_TEAPOT,
                'dst': TeapotStatuses.EMPTY_TEAPOT
            },
            {
                'name': Transistions.SCALES_EMPTY,
                'src': TeapotStatuses.EMPTY_TEAPOT,
                'dst': TeapotStatuses.EMPTY_TEAPOT
            },
            {
                'name': Transistions.WEIGHT_ABOVE_EMPTY_BELOW_FULL,
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
