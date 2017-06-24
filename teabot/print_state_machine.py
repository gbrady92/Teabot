import os
import sys
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))


def fysom_to_dot(fsm):
    """
    Takes a Fysom finite state machine representation.
    Returns a string that can be piped into the graphviz
    `dot` utility, to produce a graphical representation
    of the finite state machine.
    """
    lines = []
    for event, transitions in fsm._map.items():
        for _from, to in transitions.items():
            lines.append(
                '\t{_from} -> {to} [ label = " {event}             " ]'.format(
                    _from=_from, to=to, event=event))
    lines.sort(key=lambda l: 'FULL_TEAPOT' in l)
    return 'digraph finite_state_machine {' + '\n'.join(lines) + '\n}\n'


def print_finite_state_machine():
    from teabot.teapot_state import get_teapot_state_machine
    fsm = get_teapot_state_machine()
    print fysom_to_dot(fsm)

if __name__ == "__main__":
    print_finite_state_machine()
