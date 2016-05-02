from unittest import TestCase
from unittest import main
from teabot.status_helpers import TeapotStatus
from teabot.constants import TeapotStatuses
from mock import patch, Mock


class TestTeapotStatus(TestCase):

    def setUp(self):
        self.mock_constants = Mock()
        self.patcher = patch('teabot.status_helpers.Constants')
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_get_teapot_descriptor(self):
        teapot_status = TeapotStatus()
        result = teapot_status.get_teapot_descriptor(
            TeapotStatuses.FULL_TEAPOT, 3)
        self.assertEqual(result.teapot_state, TeapotStatuses.FULL_TEAPOT)
        self.assertEqual(result.number_of_cups_remaining, 3)
        self.assertTrue(result.timestamp)

    @patch("teabot.status_helpers.Constants")
    @patch("teabot.status_helpers.TeapotStatus.get_weight_of_tea_in_pot")
    def test_teapot_is_full_true(self, mock_get_weight, mock_constants):
        mock_constants.return_value = Mock(
            get_lower_bound_for_full_teapot=Mock(return_value=10)
        )
        mock_get_weight.return_value = 12
        teapot_status = TeapotStatus()
        result = teapot_status.teapot_is_full(20)
        self.assertTrue(result)

    @patch("teabot.status_helpers.Constants")
    @patch("teabot.status_helpers.TeapotStatus.get_weight_of_tea_in_pot")
    def test_teapot_is_full_false(self, mock_get_weight, mock_constants):
        mock_constants.return_value = Mock(
            get_lower_bound_for_full_teapot=Mock(return_value=10)
        )
        mock_get_weight.return_value = 8
        teapot_status = TeapotStatus()
        result = teapot_status.teapot_is_full(20)
        self.assertFalse(result)

    @patch("teabot.status_helpers.Constants")
    def test_teapot_is_cold_true(self, mock_constants):
        mock_constants.return_value = Mock(
            get_cold_teapot_temperature=Mock(return_value=10)
        )
        teapot_status = TeapotStatus()
        result = teapot_status.teapot_is_cold(8)
        self.assertTrue(result)

    @patch("teabot.status_helpers.Constants")
    def test_teapot_is_cold_false(self, mock_constants):
        mock_constants.return_value = Mock(
            get_cold_teapot_temperature=Mock(return_value=10)
        )
        teapot_status = TeapotStatus()
        result = teapot_status.teapot_is_cold(12)
        self.assertFalse(result)

    @patch("teabot.status_helpers.Constants")
    def test_teapot_is_empty_true(self, mock_constants):
        mock_constants.return_value = Mock(
            get_zero_weight=Mock(return_value=0),
            get_empty_teapot_weight=Mock(return_value=10)
        )
        teapot_status = TeapotStatus()
        result = teapot_status.teapot_is_empty(8)
        self.assertTrue(result)

    @patch("teabot.status_helpers.Constants")
    def test_teapot_is_empty_false(self, mock_constants):
        mock_constants.return_value = Mock(
            get_zero_weight=Mock(return_value=0),
            get_empty_teapot_weight=Mock(return_value=10)
        )
        teapot_status = TeapotStatus()
        result = teapot_status.teapot_is_empty(12)
        self.assertFalse(result)

    @patch("teabot.status_helpers.Constants")
    def test_scale_is_empty_true(self, mock_constants):
        mock_constants.return_value = Mock(
            get_zero_weight=Mock(return_value=0),
        )
        teapot_status = TeapotStatus()
        result = teapot_status.scale_is_empty(0)
        self.assertTrue(result)

    @patch("teabot.status_helpers.Constants")
    def test_scale_is_empty_false(self, mock_constants):
        mock_constants.return_value = Mock(
            get_zero_weight=Mock(return_value=0),
        )
        teapot_status = TeapotStatus()
        result = teapot_status.scale_is_empty(12)
        self.assertFalse(result)

    @patch("teabot.status_helpers.Constants")
    def test_get_weight_of_tea_in_pot(self, mock_constants):
        mock_constants.return_value = Mock(
            get_empty_teapot_weight=Mock(return_value=20),
        )
        teapot_status = TeapotStatus()
        result = teapot_status.get_weight_of_tea_in_pot(30)
        self.assertEqual(result, 10)

    @patch("teabot.status_helpers.Constants")
    @patch("teabot.status_helpers.TeapotStatus.get_weight_of_tea_in_pot")
    def test_calculate_number_of_cups_remaining(
            self, mock_get_weight, mock_constants):
        mock_constants.return_value = Mock(
            get_weight_of_tea_in_cup=Mock(return_value=2),
        )
        mock_get_weight.return_value = 20
        teapot_status = TeapotStatus()
        result = teapot_status.calculate_number_of_cups_remaining(20)
        self.assertEqual(result, 10)

    @patch("teabot.status_helpers.TeapotStatus.teapot_is_empty")
    @patch("teabot.status_helpers.TeapotStatus.teapot_is_cold")
    @patch("teabot.status_helpers.TeapotStatus.teapot_is_full")
    @patch("teabot.status_helpers.TeapotStatus.scale_is_empty")
    def test_get_teapot_status(
            self, mock_scale_empty, mock_is_full, mock_is_cold,
            mock_teapot_empty):
        teapot_status = TeapotStatus()

        # Initialy started up and scales are empty
        mock_is_full.return_value = False
        mock_is_cold.return_value = False
        mock_teapot_empty.return_value = False
        mock_scale_empty.return_value = True
        temperature_is_rising_or_constant = False
        result = teapot_status.get_teapot_status(
            10, 10, temperature_is_rising_or_constant)
        self.assertEqual(result.teapot_state, TeapotStatuses.NO_TEAPOT)

        # New teapot put on the scales
        mock_is_full.return_value = True
        mock_is_cold.return_value = False
        mock_teapot_empty.return_value = False
        mock_scale_empty.return_value = False
        temperature_is_rising_or_constant = True
        result = teapot_status.get_teapot_status(
            10, 10, temperature_is_rising_or_constant)
        self.assertEqual(result.teapot_state, TeapotStatuses.FULL_TEAPOT)

        # Teapot lifted from scales to pour cup
        mock_is_full.return_value = False
        mock_is_cold.return_value = False
        mock_teapot_empty.return_value = False
        mock_scale_empty.return_value = True
        temperature_is_rising_or_constant = True
        result = teapot_status.get_teapot_status(
            10, 10, temperature_is_rising_or_constant)
        self.assertEqual(result.teapot_state, TeapotStatuses.FULL_TEAPOT)

        # New cup poured
        mock_is_full.return_value = False
        mock_is_cold.return_value = False
        mock_teapot_empty.return_value = False
        mock_scale_empty.return_value = False
        temperature_is_rising_or_constant = True
        result = teapot_status.get_teapot_status(
            10, 10, temperature_is_rising_or_constant)
        self.assertEqual(result.teapot_state, TeapotStatuses.GOOD_TEAPOT)

        # Teapot lifted from scales to pour another cup
        mock_is_full.return_value = False
        mock_is_cold.return_value = False
        mock_teapot_empty.return_value = False
        mock_scale_empty.return_value = True
        temperature_is_rising_or_constant = True
        result = teapot_status.get_teapot_status(
            10, 10, temperature_is_rising_or_constant)
        self.assertEqual(result.teapot_state, TeapotStatuses.GOOD_TEAPOT)

        # All the tea drunk
        mock_is_full.return_value = False
        mock_is_cold.return_value = False
        mock_teapot_empty.return_value = True
        mock_scale_empty.return_value = False
        temperature_is_rising_or_constant = False
        result = teapot_status.get_teapot_status(
            10, 10, temperature_is_rising_or_constant)
        self.assertEqual(result.teapot_state, TeapotStatuses.EMPTY_TEAPOT)

        # Teapot lifted from scales to refill
        mock_is_full.return_value = False
        mock_is_cold.return_value = True
        mock_teapot_empty.return_value = False
        mock_scale_empty.return_value = True
        temperature_is_rising_or_constant = False
        result = teapot_status.get_teapot_status(
            10, 10, temperature_is_rising_or_constant)
        self.assertEqual(result.teapot_state, TeapotStatuses.EMPTY_TEAPOT)

        # Teapot refilled
        mock_is_full.return_value = True
        mock_is_cold.return_value = False
        mock_teapot_empty.return_value = False
        mock_scale_empty.return_value = False
        temperature_is_rising_or_constant = True
        result = teapot_status.get_teapot_status(
            10, 10, temperature_is_rising_or_constant)
        self.assertEqual(result.teapot_state, TeapotStatuses.FULL_TEAPOT)

        # Cup drunk
        mock_is_full.return_value = False
        mock_is_cold.return_value = False
        mock_teapot_empty.return_value = False
        mock_scale_empty.return_value = False
        temperature_is_rising_or_constant = True
        result = teapot_status.get_teapot_status(
            10, 10, temperature_is_rising_or_constant)
        self.assertEqual(result.teapot_state, TeapotStatuses.GOOD_TEAPOT)

        # Teapot goes cold :(
        mock_is_full.return_value = False
        mock_is_cold.return_value = True
        mock_teapot_empty.return_value = False
        mock_scale_empty.return_value = False
        temperature_is_rising_or_constant = False
        result = teapot_status.get_teapot_status(
            10, 10, temperature_is_rising_or_constant)
        self.assertEqual(result.teapot_state, TeapotStatuses.COLD_TEAPOT)

        # Lifted off for pouring
        mock_is_full.return_value = False
        mock_is_cold.return_value = True
        mock_teapot_empty.return_value = False
        mock_scale_empty.return_value = True
        temperature_is_rising_or_constant = False
        result = teapot_status.get_teapot_status(
            10, 10, temperature_is_rising_or_constant)
        self.assertEqual(result.teapot_state, TeapotStatuses.COLD_TEAPOT)

        # Cold tea drunk
        mock_is_full.return_value = False
        mock_is_cold.return_value = True
        mock_teapot_empty.return_value = True
        mock_scale_empty.return_value = False
        temperature_is_rising_or_constant = False
        result = teapot_status.get_teapot_status(
            10, 10, temperature_is_rising_or_constant)
        self.assertEqual(result.teapot_state, TeapotStatuses.EMPTY_TEAPOT)

        # Teapot refilled
        mock_is_full.return_value = True
        mock_is_cold.return_value = False
        mock_teapot_empty.return_value = False
        mock_scale_empty.return_value = False
        temperature_is_rising_or_constant = True
        result = teapot_status.get_teapot_status(
            10, 10, temperature_is_rising_or_constant)
        self.assertEqual(result.teapot_state, TeapotStatuses.FULL_TEAPOT)

        # Cup drunk
        mock_is_full.return_value = False
        mock_is_cold.return_value = False
        mock_teapot_empty.return_value = False
        mock_scale_empty.return_value = False
        temperature_is_rising_or_constant = True
        result = teapot_status.get_teapot_status(
            10, 10, temperature_is_rising_or_constant)
        self.assertEqual(result.teapot_state, TeapotStatuses.GOOD_TEAPOT)

        # Teapot goes cold :(
        mock_is_full.return_value = False
        mock_is_cold.return_value = True
        mock_teapot_empty.return_value = False
        mock_scale_empty.return_value = False
        temperature_is_rising_or_constant = False
        result = teapot_status.get_teapot_status(
            10, 10, temperature_is_rising_or_constant)
        self.assertEqual(result.teapot_state, TeapotStatuses.COLD_TEAPOT)

        # Teapot refilled
        mock_is_full.return_value = True
        mock_is_cold.return_value = False
        mock_teapot_empty.return_value = False
        mock_scale_empty.return_value = False
        temperature_is_rising_or_constant = True
        result = teapot_status.get_teapot_status(
            10, 10, temperature_is_rising_or_constant)
        self.assertEqual(result.teapot_state, TeapotStatuses.FULL_TEAPOT)

        # Lifted off for pouring
        mock_is_full.return_value = False
        mock_is_cold.return_value = True
        mock_teapot_empty.return_value = False
        mock_scale_empty.return_value = True
        temperature_is_rising_or_constant = False
        result = teapot_status.get_teapot_status(
            10, 10, temperature_is_rising_or_constant)
        self.assertEqual(result.teapot_state, TeapotStatuses.FULL_TEAPOT)

        # Entire teapot drunk
        mock_is_full.return_value = False
        mock_is_cold.return_value = False
        mock_teapot_empty.return_value = True
        mock_scale_empty.return_value = False
        temperature_is_rising_or_constant = True
        result = teapot_status.get_teapot_status(
            10, 10, temperature_is_rising_or_constant)
        self.assertEqual(result.teapot_state, TeapotStatuses.EMPTY_TEAPOT)


if __name__ == '__main__':
    main()
