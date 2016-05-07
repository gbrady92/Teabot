from unittest import TestCase
from unittest import main
from teabot.inputs.temperature import Temperature
from mock import patch


class TestTemperature(TestCase):

    def setUp(self):
        self.mock_glob = patch("teabot.inputs.temperature.glob")
        self.mock_os = patch("teabot.inputs.temperature.os")
        self.mock_glob.start()
        self.mock_os.start()

    def tearDown(self):
        self.mock_glob.stop()
        self.mock_os.stop()

    def test_pairwise(self):
        lst = [1, 2, 3, 4]
        pairs = Temperature().pairwise(lst)
        self.assertEqual(pairs, [(1, 2), (2, 3), (3, 4)])

    @patch("teabot.inputs.temperature.Temperature.get_reading", auto_spec=True)
    def test_is_rising_or_constant_true(self, mock_get_reading):
        mock_get_reading.side_effect = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        result = Temperature().is_rising_or_constant()
        self.assertTrue(result)

    @patch("teabot.inputs.temperature.Temperature.get_reading", auto_spec=True)
    def test_is_rising_or_constant_false(self, mock_get_reading):
        mock_get_reading.side_effect = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        result = Temperature().is_rising_or_constant()
        self.assertFalse(result)


if __name__ == '__main__':
    main()
