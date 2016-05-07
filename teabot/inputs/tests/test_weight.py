from unittest import TestCase
from unittest import main
from teabot.inputs.weight import Weight
from mock import patch


class TestWeight(TestCase):

    def setUp(self):
        self.mock_usb = patch("teabot.inputs.weight.usb", auto_spec=True)
        self.mock_usb.start()

    def tearDown(self):
        self.mock_usb.stop()

    def test_most_common(self):
        lst = [1, 2, 3, 4, 4]
        result = Weight().most_common(lst)
        self.assertEqual(result, 4)


if __name__ == '__main__':
    main()
