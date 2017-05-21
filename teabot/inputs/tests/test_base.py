from datetime import timedelta
from mock import patch
from unittest import TestCase

from teabot.inputs.base import BaseSensor


@patch("teabot.inputs.base.BaseSensor.POLL_PERIOD", timedelta())
class TestBase(TestCase):

    def test_pairwise(self):
        lst = [1, 2, 3, 4]
        pairs = BaseSensor()._pairwise(lst)
        self.assertEqual(pairs, [(1, 2), (2, 3), (3, 4)])

    @patch("teabot.inputs.base.BaseSensor.read_sensor", autospec=True)
    def test_is_rising_or_constant_true(self, mock_read_sensor):
        mock_read_sensor.side_effect = iter([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        result = BaseSensor().is_rising_or_constant()
        self.assertTrue(result)

    @patch("teabot.inputs.base.BaseSensor.read_sensor", autospec=True)
    def test_is_rising_or_constant_false(self, mock_read_sensor):
        mock_read_sensor.side_effect = iter([10, 9, 8, 7, 6, 5, 4, 3, 2, 1])
        result = BaseSensor().is_rising_or_constant()
        self.assertFalse(result)
