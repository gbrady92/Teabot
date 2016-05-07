from unittest import TestCase
from unittest import main
from teabot.constants import Constants
from mock import patch


class TestConstants(TestCase):

    @patch("teabot.constants.Constants.get_full_teapot_weight", auto_spec=True)
    @patch("teabot.constants.Constants.get_empty_teapot_weight",
           auto_spec=True)
    def test_get_weight_of_tea_in_full_teapot(self, mock_empty, mock_full):
        mock_empty.return_value = 20
        mock_full.return_value = 100
        result = Constants().get_weight_of_tea_in_full_teapot()
        self.assertEqual(result, 80)

    @patch("teabot.constants.Constants.get_full_teapot_weight", auto_spec=True)
    @patch("teabot.constants.Constants.get_empty_teapot_weight",
           auto_spec=True)
    @patch("teabot.constants.Constants.get_weight_of_tea_in_cup",
           auto_spec=True)
    def test_get_lower_bound_for_full_teapot(
            self, mock_cup, mock_empty, mock_full):
        mock_cup.return_value = 5
        mock_empty.return_value = 20
        mock_full.return_value = 100
        result = Constants().get_lower_bound_for_full_teapot()
        self.assertEqual(result, 78)


if __name__ == '__main__':
    main()
