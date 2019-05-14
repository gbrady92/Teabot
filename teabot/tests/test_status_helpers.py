from unittest import TestCase
from unittest import main
from datetime import datetime, timedelta
from teabot.status_helpers import TeapotStatus
from teabot.constants import TeapotStatuses
from mock import patch, Mock
from teabot.teapot_state import generate_teapot_state_machine


class TestTeapotStatus(TestCase):

    def setUp(self):
        self.mock_constants = Mock()
        self.patcher = patch('teabot.status_helpers.Constants', auto_spec=True)
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

    @patch("teabot.status_helpers.Constants", auto_spec=True)
    @patch("teabot.status_helpers.TeapotStatus.get_weight_of_tea_in_pot",
           auto_spec=True)
    def test_teapot_is_full_true(self, mock_get_weight, mock_constants):
        mock_constants.return_value = Mock(
            get_lower_bound_for_full_teapot=Mock(return_value=10)
        )
        mock_get_weight.return_value = 12
        teapot_status = TeapotStatus()
        result = teapot_status.teapot_is_full(20)
        self.assertTrue(result)

    @patch("teabot.status_helpers.Constants", auto_spec=True)
    @patch("teabot.status_helpers.TeapotStatus.get_weight_of_tea_in_pot",
           auto_spec=True)
    def test_teapot_is_full_false(self, mock_get_weight, mock_constants):
        mock_constants.return_value = Mock(
            get_lower_bound_for_full_teapot=Mock(return_value=10)
        )
        mock_get_weight.return_value = 8
        teapot_status = TeapotStatus()
        result = teapot_status.teapot_is_full(20)
        self.assertFalse(result)

    @patch("teabot.status_helpers.Constants", auto_spec=True)
    def test_teapot_is_empty_true(self, mock_constants):
        mock_constants.return_value = Mock(
            get_zero_weight=Mock(return_value=0),
            get_empty_teapot_weight=Mock(return_value=10)
        )
        teapot_status = TeapotStatus()
        result = teapot_status.teapot_is_empty(8)
        self.assertTrue(result)

    @patch("teabot.status_helpers.Constants", auto_spec=True)
    def test_teapot_is_empty_false(self, mock_constants):
        mock_constants.return_value = Mock(
            get_zero_weight=Mock(return_value=0),
            get_empty_teapot_weight=Mock(return_value=10)
        )
        teapot_status = TeapotStatus()
        result = teapot_status.teapot_is_empty(12)
        self.assertFalse(result)

    @patch("teabot.status_helpers.Constants", auto_spec=True)
    def test_scale_is_empty_true(self, mock_constants):
        mock_constants.return_value = Mock(
            get_zero_weight=Mock(return_value=0),
        )
        teapot_status = TeapotStatus()
        result = teapot_status.scale_is_empty(0)
        self.assertTrue(result)

    @patch("teabot.status_helpers.Constants", auto_spec=True)
    def test_scale_is_empty_false(self, mock_constants):
        mock_constants.return_value = Mock(
            get_zero_weight=Mock(return_value=0),
        )
        teapot_status = TeapotStatus()
        result = teapot_status.scale_is_empty(12)
        self.assertFalse(result)

    @patch("teabot.status_helpers.Constants", auto_spec=True)
    def test_get_weight_of_tea_in_pot(self, mock_constants):
        mock_constants.return_value = Mock(
            get_empty_teapot_weight=Mock(return_value=20),
        )
        teapot_status = TeapotStatus()
        result = teapot_status.get_weight_of_tea_in_pot(30)
        self.assertEqual(result, 10)

    @patch("teabot.status_helpers.Constants", auto_spec=True)
    def test_get_weight_of_tea_in_pot_empty_scales(self, mock_constants):
        mock_constants.return_value = Mock(
            get_empty_teapot_weight=Mock(return_value=20),
        )
        teapot_status = TeapotStatus()
        result = teapot_status.get_weight_of_tea_in_pot(0)
        self.assertEqual(result, 0)

    @patch("teabot.status_helpers.Constants", auto_spec=True)
    @patch("teabot.status_helpers.TeapotStatus.get_weight_of_tea_in_pot",
           auto_spec=True)
    def test_calculate_number_of_cups_remaining_whole_cups(
            self, mock_get_weight, mock_constants):
        mock_constants.return_value = Mock(
            get_weight_of_tea_in_cup=Mock(return_value=2),
        )
        mock_get_weight.return_value = 20
        teapot_status = TeapotStatus()
        result = teapot_status.calculate_number_of_cups_remaining(20)
        self.assertEqual(result, 10)

    @patch("teabot.status_helpers.Constants", auto_spec=True)
    @patch("teabot.status_helpers.TeapotStatus.get_weight_of_tea_in_pot",
           auto_spec=True)
    def test_calculate_number_of_cups_remaining_greater_than_half(
            self, mock_get_weight, mock_constants):
        mock_constants.return_value = Mock(
            get_weight_of_tea_in_cup=Mock(return_value=3),
        )
        mock_get_weight.return_value = 20
        teapot_status = TeapotStatus()
        result = teapot_status.calculate_number_of_cups_remaining(20)
        self.assertEqual(result, 7)

    @patch("teabot.status_helpers.Constants", auto_spec=True)
    @patch("teabot.status_helpers.TeapotStatus.get_weight_of_tea_in_pot",
           auto_spec=True)
    def test_calculate_number_of_cups_remaining_less_than_half(
            self, mock_get_weight, mock_constants):
        mock_constants.return_value = Mock(
            get_weight_of_tea_in_cup=Mock(return_value=6),
        )
        mock_get_weight.return_value = 20
        teapot_status = TeapotStatus()
        result = teapot_status.calculate_number_of_cups_remaining(20)
        self.assertEqual(result, 3)

    @patch("teabot.status_helpers.TeapotStatus.teapot_is_empty",
           auto_spec=True)
    @patch("teabot.status_helpers.TeapotStatus.teapot_is_full", auto_spec=True)
    @patch("teabot.status_helpers.TeapotStatus.scale_is_empty", auto_spec=True)
    def test_get_teapot_status(
            self, mock_scale_empty, mock_is_full, mock_teapot_empty):
        teapot_status = TeapotStatus()
        now = datetime.now()

        # Initialy started up and scales are empty
        mock_is_full.return_value = False
        mock_teapot_empty.return_value = False
        mock_scale_empty.return_value = True
        result = teapot_status.get_teapot_status(10, datetime.min)
        self.assertEqual(result.teapot_state, TeapotStatuses.NO_TEAPOT)

        # New teapot put on the scales
        mock_is_full.return_value = True
        mock_teapot_empty.return_value = False
        mock_scale_empty.return_value = False
        result = teapot_status.get_teapot_status(10, now)
        self.assertEqual(result.teapot_state, TeapotStatuses.FULL_TEAPOT)

        # Teapot lifted from scales to pour cup
        mock_is_full.return_value = False
        mock_teapot_empty.return_value = False
        mock_scale_empty.return_value = True
        result = teapot_status.get_teapot_status(10, now)
        self.assertEqual(result.teapot_state, TeapotStatuses.FULL_TEAPOT)

        # New cup poured
        mock_is_full.return_value = False
        mock_teapot_empty.return_value = False
        mock_scale_empty.return_value = False
        result = teapot_status.get_teapot_status(10, now)
        self.assertEqual(result.teapot_state, TeapotStatuses.GOOD_TEAPOT)

        # Teapot lifted from scales to pour another cup
        mock_is_full.return_value = False
        mock_teapot_empty.return_value = False
        mock_scale_empty.return_value = True
        result = teapot_status.get_teapot_status(10, now)
        self.assertEqual(result.teapot_state, TeapotStatuses.GOOD_TEAPOT)

        # All the tea drunk
        mock_is_full.return_value = False
        mock_teapot_empty.return_value = True
        mock_scale_empty.return_value = False
        result = teapot_status.get_teapot_status(10, now)
        self.assertEqual(result.teapot_state, TeapotStatuses.EMPTY_TEAPOT)

        # Teapot lifted from scales to refill
        mock_is_full.return_value = False
        mock_teapot_empty.return_value = False
        mock_scale_empty.return_value = True
        result = teapot_status.get_teapot_status(10, now)
        self.assertEqual(result.teapot_state, TeapotStatuses.EMPTY_TEAPOT)

        # Teapot refilled
        mock_is_full.return_value = True
        mock_teapot_empty.return_value = False
        mock_scale_empty.return_value = False
        result = teapot_status.get_teapot_status(
            10, now + timedelta(minutes=2))
        self.assertEqual(result.teapot_state, TeapotStatuses.FULL_TEAPOT)

        # Cup drunk
        mock_is_full.return_value = False
        mock_teapot_empty.return_value = False
        mock_scale_empty.return_value = False
        result = teapot_status.get_teapot_status(
            10, now + timedelta(minutes=2))
        self.assertEqual(result.teapot_state, TeapotStatuses.GOOD_TEAPOT)

        # Cold tea drunk
        mock_is_full.return_value = False
        mock_teapot_empty.return_value = True
        mock_scale_empty.return_value = False
        result = teapot_status.get_teapot_status(
            10, now + timedelta(minutes=2))
        self.assertEqual(result.teapot_state, TeapotStatuses.EMPTY_TEAPOT)

        # Teapot refilled
        mock_is_full.return_value = True
        mock_teapot_empty.return_value = False
        mock_scale_empty.return_value = False
        result = teapot_status.get_teapot_status(
            10, now + timedelta(minutes=4))
        self.assertEqual(result.teapot_state, TeapotStatuses.FULL_TEAPOT)

        # Cup drunk
        mock_is_full.return_value = False
        mock_teapot_empty.return_value = False
        mock_scale_empty.return_value = False
        result = teapot_status.get_teapot_status(
            10, now + timedelta(minutes=4))
        self.assertEqual(result.teapot_state, TeapotStatuses.GOOD_TEAPOT)

        # Teapot refilled
        mock_is_full.return_value = True
        mock_teapot_empty.return_value = False
        mock_scale_empty.return_value = False
        result = teapot_status.get_teapot_status(
            10, now + timedelta(minutes=6))
        self.assertEqual(result.teapot_state, TeapotStatuses.FULL_TEAPOT)

        # Lifted off for pouring
        mock_is_full.return_value = False
        mock_teapot_empty.return_value = False
        mock_scale_empty.return_value = True
        result = teapot_status.get_teapot_status(
            10, now + timedelta(minutes=6))
        self.assertEqual(result.teapot_state, TeapotStatuses.FULL_TEAPOT)

        # Entire teapot drunk
        mock_is_full.return_value = False
        mock_teapot_empty.return_value = True
        mock_scale_empty.return_value = False
        result = teapot_status.get_teapot_status(
            10, now + timedelta(minutes=6))
        self.assertEqual(result.teapot_state, TeapotStatuses.EMPTY_TEAPOT)

        # Teapot refilled
        mock_is_full.return_value = True
        mock_teapot_empty.return_value = False
        mock_scale_empty.return_value = False
        result = teapot_status.get_teapot_status(
            10, now + timedelta(minutes=8))
        self.assertEqual(result.teapot_state, TeapotStatuses.FULL_TEAPOT)

        # Cup drunk
        mock_is_full.return_value = False
        mock_teapot_empty.return_value = False
        mock_scale_empty.return_value = False
        result = teapot_status.get_teapot_status(
            10, now + timedelta(minutes=8))
        self.assertEqual(result.teapot_state, TeapotStatuses.GOOD_TEAPOT)

        # Teapot refilled
        mock_is_full.return_value = True
        mock_teapot_empty.return_value = False
        mock_scale_empty.return_value = False
        result = teapot_status.get_teapot_status(
            10, now + timedelta(minutes=10))
        self.assertEqual(result.teapot_state, TeapotStatuses.FULL_TEAPOT)

        # Full teapot sits there
        mock_is_full.return_value = True
        mock_teapot_empty.return_value = False
        mock_scale_empty.return_value = False
        result = teapot_status.get_teapot_status(
            10, now + timedelta(minutes=10))
        self.assertEqual(result.teapot_state, TeapotStatuses.GOOD_TEAPOT)

        # Full teapot is drank and now teapot is empty
        mock_is_full.return_value = False
        mock_teapot_empty.return_value = True
        mock_scale_empty.return_value = False
        result = teapot_status.get_teapot_status(
            10, now + timedelta(minutes=10))
        self.assertEqual(result.teapot_state, TeapotStatuses.EMPTY_TEAPOT)

        # Good teapot placed on scales
        mock_is_full.return_value = False
        mock_teapot_empty.return_value = False
        mock_scale_empty.return_value = False
        result = teapot_status.get_teapot_status(
            10, now + timedelta(minutes=10))
        self.assertEqual(result.teapot_state, TeapotStatuses.GOOD_TEAPOT)

    @patch("teabot.status_helpers.TeapotStatus.teapot_is_empty",
           auto_spec=True)
    @patch("teabot.status_helpers.TeapotStatus.teapot_is_full", auto_spec=True)
    @patch("teabot.status_helpers.TeapotStatus.scale_is_empty", auto_spec=True)
    @patch("teabot.status_helpers.get_teapot_state_machine", auto_spec=True)
    def test_get_teapot_status_nothing_to_empty(
            self, mock_state_machine, mock_scale_empty, mock_is_full,
            mock_teapot_empty):
        mock_state_machine.return_value = generate_teapot_state_machine()
        teapot_status = TeapotStatus()

        # Initialy started up and scales are empty
        mock_is_full.return_value = False
        mock_scale_empty.return_value = True
        result = teapot_status.get_teapot_status(10, datetime.min)
        self.assertEqual(result.teapot_state, TeapotStatuses.NO_TEAPOT)

        # Empty teapot places on scales
        mock_is_full.return_value = False
        mock_teapot_empty.return_value = True
        mock_scale_empty.return_value = False
        result = teapot_status.get_teapot_status(10, datetime.now())
        self.assertEqual(result.teapot_state, TeapotStatuses.EMPTY_TEAPOT)

    @patch("teabot.status_helpers.TeapotStatus.teapot_is_empty",
           auto_spec=True)
    @patch("teabot.status_helpers.TeapotStatus.teapot_is_full", auto_spec=True)
    @patch("teabot.status_helpers.TeapotStatus.scale_is_empty", auto_spec=True)
    @patch("teabot.status_helpers.get_teapot_state_machine", auto_spec=True)
    def test_get_teapot_status_nothing_to_cold(
            self, mock_state_machine, mock_scale_empty, mock_is_full,
            mock_teapot_empty):
        mock_state_machine.return_value = generate_teapot_state_machine()
        teapot_status = TeapotStatus()

        # Initialy started up and scales are empty
        mock_is_full.return_value = False
        mock_teapot_empty.return_value = False
        mock_scale_empty.return_value = True
        result = teapot_status.get_teapot_status(10, datetime.min)
        self.assertEqual(result.teapot_state, TeapotStatuses.NO_TEAPOT)

    @patch("teabot.status_helpers.TeapotStatus.teapot_is_empty",
           auto_spec=True)
    @patch("teabot.status_helpers.TeapotStatus.teapot_is_full", auto_spec=True)
    @patch("teabot.status_helpers.TeapotStatus.scale_is_empty", auto_spec=True)
    @patch("teabot.status_helpers.get_teapot_state_machine", auto_spec=True)
    def test_get_teapot_status_nothing_to_good(
            self, mock_state_machine, mock_scale_empty, mock_is_full,
            mock_teapot_empty):
        mock_state_machine.return_value = generate_teapot_state_machine()
        teapot_status = TeapotStatus()

        # Initialy started up and scales are empty
        mock_is_full.return_value = False
        mock_teapot_empty.return_value = False
        mock_scale_empty.return_value = True
        result = teapot_status.get_teapot_status(10, datetime.min)
        self.assertEqual(result.teapot_state, TeapotStatuses.NO_TEAPOT)

        # Good teapot placed on scales
        mock_is_full.return_value = False
        mock_teapot_empty.return_value = False
        mock_scale_empty.return_value = False
        result = teapot_status.get_teapot_status(
            10, datetime.now())
        self.assertEqual(result.teapot_state, TeapotStatuses.GOOD_TEAPOT)

    @patch("teabot.status_helpers.Constants", auto_spec=True)
    @patch(
        "teabot.status_helpers.TeapotStatus.get_current_time", auto_spec=True)
    def test_new_teapot_is_not_duplicate(self, mock_now, mock_constants):
        mock_now.side_effect = iter([
            datetime(2016, 1, 1, 12, 0, 0),
            datetime(2016, 1, 1, 12, 1, 0),
        ])
        mock_constants.return_value = Mock(
            get_new_teapot_refresh_period=Mock(
                return_value=timedelta(minutes=10)
            )
        )
        teapot_status = TeapotStatus()
        result = teapot_status.new_teapot_is_not_duplicate()
        self.assertTrue(result)

        result = teapot_status.new_teapot_is_not_duplicate()
        self.assertFalse(result)

    @patch("teabot.status_helpers.Constants", auto_spec=True)
    @patch(
        "teabot.status_helpers.TeapotStatus.get_current_time", auto_spec=True)
    @patch("teabot.status_helpers.TeapotStatus.teapot_is_empty",
           auto_spec=True)
    @patch("teabot.status_helpers.TeapotStatus.teapot_is_full", auto_spec=True)
    @patch("teabot.status_helpers.TeapotStatus.scale_is_empty", auto_spec=True)
    @patch("teabot.status_helpers.get_teapot_state_machine", auto_spec=True)
    def test_get_teapot_status_no_duplicate_full_pots(
            self, mock_state_machine, mock_scale_empty, mock_is_full,
            mock_teapot_empty, mock_now, mock_constants):

        mock_now.side_effect = iter([
            datetime(2016, 1, 1, 12, 29, 0),
            datetime(2016, 1, 1, 12, 30, 0),
            datetime(2016, 1, 1, 12, 50, 0)
        ])
        mock_constants.return_value = Mock(
            get_new_teapot_refresh_period=Mock(
                return_value=timedelta(minutes=10)
            ),
            get_empty_teapot_weight=Mock(
                return_value=10
            ),
            get_weight_of_tea_in_cup=Mock(
                return_value=10
            )
        )
        mock_state_machine.return_value = generate_teapot_state_machine()
        teapot_status = TeapotStatus()

        now = datetime.now()

        # Initialy started up and scales are empty
        mock_is_full.return_value = False
        mock_teapot_empty.return_value = False
        mock_scale_empty.return_value = True
        result = teapot_status.get_teapot_status(
            10, datetime.min)
        self.assertEqual(result.teapot_state, TeapotStatuses.NO_TEAPOT)

        # Full teapot placed on scales
        mock_is_full.return_value = True
        mock_teapot_empty.return_value = False
        mock_scale_empty.return_value = False
        result = teapot_status.get_teapot_status(
            10, now)
        self.assertEqual(result.teapot_state, TeapotStatuses.FULL_TEAPOT)

        # Full teapot lifted and placed down again
        mock_is_full.return_value = True
        mock_teapot_empty.return_value = False
        mock_scale_empty.return_value = False
        result = teapot_status.get_teapot_status(
            10, now)
        self.assertEqual(result.teapot_state, TeapotStatuses.GOOD_TEAPOT)

        # New teapot made
        mock_is_full.return_value = True
        mock_teapot_empty.return_value = False
        mock_scale_empty.return_value = False
        result = teapot_status.get_teapot_status(
            10,
            now + timedelta(minutes=2))
        self.assertEqual(result.teapot_state, TeapotStatuses.FULL_TEAPOT)


if __name__ == '__main__':
    main()
