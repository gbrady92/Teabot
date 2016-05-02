from unittest import TestCase
from unittest import main
from constants import Constants
from mock import patch


class TestConstants(TestCase):

    @patch("constants.Constants.get_full_teapot_weight")
    @patch("constants.Constants.get_empty_teapot_weight")
    def test_get_weight_of_tea_in_full_teapot(self, mock_empty, mock_full):
        mock_empty.return_value = 20
        mock_full.return_value = 100
        result = Constants().get_weight_of_tea_in_full_teapot()
        self.assertEqual(result, 80)

    @patch("constants.Constants.get_full_teapot_weight")
    @patch("constants.Constants.get_empty_teapot_weight")
    @patch("constants.Constants.get_weight_of_tea_in_cup")
    def test_get_lower_bound_for_full_teapot(
            self, mock_cup, mock_empty, mock_full):
        mock_cup.return_value = 5
        mock_empty.return_value = 20
        mock_full.return_value = 100
        result = Constants().get_lower_bound_for_full_teapot()
        self.assertEqual(result, 75)


if __name__ == '__main__':
    main()
