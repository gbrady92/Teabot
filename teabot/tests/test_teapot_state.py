from unittest import TestCase
from unittest import main
from teabot.teapot_state import generate_teapot_state_machine, \
    get_teapot_state_machine
from teabot.constants import TeapotStatuses


class TestTeapotState(TestCase):

    def _get_state_machine_at_initial_state(self):
        return generate_teapot_state_machine()

    def _get_state_machine_at_full_teapot(self):
        state_machine = generate_teapot_state_machine()
        state_machine.temp_rising_weight_above_full()
        return state_machine

    def _get_state_machine_at_good_teapot(self):
        state_machine = generate_teapot_state_machine()
        state_machine.temp_rising_weight_above_full()
        state_machine.weight_above_empty_below_full()
        return state_machine

    def _get_state_machine_at_empty_teapot(self):
        state_machine = generate_teapot_state_machine()
        state_machine.temp_rising_weight_above_full()
        state_machine.weight_above_empty_below_full()
        state_machine.weight_below_empty()
        return state_machine

    def _get_state_machine_at_cold_teapot(self):
        state_machine = generate_teapot_state_machine()
        state_machine.temp_rising_weight_above_full()
        state_machine.weight_above_empty_below_full()
        state_machine.temp_below_cold_weight_above_empty()
        return state_machine

    def test_get_teapot_state_machine(self):
        state_machine = get_teapot_state_machine()
        state_machine_again = get_teapot_state_machine()
        self.assertTrue(state_machine is state_machine_again)

    def test_initial_state(self):
        state_machine = self._get_state_machine_at_initial_state()
        self.assertEqual(state_machine.current, TeapotStatuses.NO_TEAPOT)

        # Teapot placed on scales
        state_machine.temp_rising_weight_above_full()
        self.assertEqual(
            state_machine.current,
            TeapotStatuses.FULL_TEAPOT
        )

        # Should stay where we are
        state_machine = self._get_state_machine_at_initial_state()
        self.assertEqual(state_machine.current, TeapotStatuses.NO_TEAPOT)

        # Teapot lifted off scales
        state_machine.scales_empty()
        self.assertEqual(
            state_machine.current,
            TeapotStatuses.NO_TEAPOT
        )

    def test_full_teapot(self):
        state_machine = self._get_state_machine_at_full_teapot()
        self.assertEqual(state_machine.current, TeapotStatuses.FULL_TEAPOT)

        # Cup of tea poured
        state_machine.weight_above_empty_below_full()
        self.assertEqual(
            state_machine.current,
            TeapotStatuses.GOOD_TEAPOT
        )

        state_machine = self._get_state_machine_at_full_teapot()
        self.assertEqual(state_machine.current, TeapotStatuses.FULL_TEAPOT)

        # Teapot goes cold
        state_machine.temp_below_cold()
        self.assertEqual(
            state_machine.current,
            TeapotStatuses.COLD_TEAPOT
        )

        state_machine = self._get_state_machine_at_full_teapot()
        self.assertEqual(state_machine.current, TeapotStatuses.FULL_TEAPOT)

        # Entire teapot poured in one go
        state_machine.weight_below_empty()
        self.assertEqual(
            state_machine.current,
            TeapotStatuses.EMPTY_TEAPOT
        )

        state_machine = self._get_state_machine_at_full_teapot()
        self.assertEqual(state_machine.current, TeapotStatuses.FULL_TEAPOT)

        # Teapot lifted off scales for pouring
        state_machine.scales_empty()
        self.assertEqual(
            state_machine.current,
            TeapotStatuses.FULL_TEAPOT
        )

    def test_good_teapot(self):
        state_machine = self._get_state_machine_at_good_teapot()
        self.assertEqual(state_machine.current, TeapotStatuses.GOOD_TEAPOT)

        # Another cup of tea poured and still not empty
        state_machine.weight_above_empty_below_full()
        self.assertEqual(
            state_machine.current,
            TeapotStatuses.GOOD_TEAPOT
        )

        state_machine = self._get_state_machine_at_good_teapot()
        self.assertEqual(state_machine.current, TeapotStatuses.GOOD_TEAPOT)

        # All the teas gone
        state_machine.weight_below_empty()
        self.assertEqual(
            state_machine.current,
            TeapotStatuses.EMPTY_TEAPOT
        )

        state_machine = self._get_state_machine_at_good_teapot()
        self.assertEqual(state_machine.current, TeapotStatuses.GOOD_TEAPOT)

        # Good pot has gone cold
        state_machine.temp_below_cold_weight_above_empty()
        self.assertEqual(
            state_machine.current,
            TeapotStatuses.COLD_TEAPOT
        )

        state_machine = self._get_state_machine_at_good_teapot()
        self.assertEqual(state_machine.current, TeapotStatuses.GOOD_TEAPOT)

        # Pot lifted off for pouring
        state_machine.scales_empty()
        self.assertEqual(
            state_machine.current,
            TeapotStatuses.GOOD_TEAPOT
        )

    def test_empty_teapot(self):
        state_machine = self._get_state_machine_at_empty_teapot()
        self.assertEqual(state_machine.current, TeapotStatuses.EMPTY_TEAPOT)

        # New pot made
        state_machine.temp_rising_weight_above_full()
        self.assertEqual(
            state_machine.current,
            TeapotStatuses.FULL_TEAPOT
        )

        state_machine = self._get_state_machine_at_empty_teapot()
        self.assertEqual(state_machine.current, TeapotStatuses.EMPTY_TEAPOT)

        # Empty pot sits on scales
        state_machine.weight_below_empty()
        self.assertEqual(
            state_machine.current,
            TeapotStatuses.EMPTY_TEAPOT
        )

        state_machine = self._get_state_machine_at_empty_teapot()
        self.assertEqual(state_machine.current, TeapotStatuses.EMPTY_TEAPOT)

        # Empty pot lifted off scales
        state_machine.scales_empty()
        self.assertEqual(
            state_machine.current,
            TeapotStatuses.EMPTY_TEAPOT
        )

    def test_cold_teapot(self):
        state_machine = self._get_state_machine_at_cold_teapot()
        self.assertEqual(state_machine.current, TeapotStatuses.COLD_TEAPOT)

        # New pot made
        state_machine.temp_rising_weight_above_full()
        self.assertEqual(
            state_machine.current,
            TeapotStatuses.FULL_TEAPOT
        )

        state_machine = self._get_state_machine_at_cold_teapot()
        self.assertEqual(state_machine.current, TeapotStatuses.COLD_TEAPOT)

        # Cold pot drank
        state_machine.weight_below_empty()
        self.assertEqual(
            state_machine.current,
            TeapotStatuses.EMPTY_TEAPOT
        )

        state_machine = self._get_state_machine_at_cold_teapot()
        self.assertEqual(state_machine.current, TeapotStatuses.COLD_TEAPOT)

        # Cold pot lifted off scales
        state_machine.scales_empty()
        self.assertEqual(
            state_machine.current,
            TeapotStatuses.COLD_TEAPOT
        )

        state_machine = self._get_state_machine_at_cold_teapot()
        self.assertEqual(state_machine.current, TeapotStatuses.COLD_TEAPOT)

        # Cold pot its on scales
        state_machine.temp_below_cold_weight_above_empty()
        self.assertEqual(
            state_machine.current,
            TeapotStatuses.COLD_TEAPOT
        )

if __name__ == '__main__':
    main()
