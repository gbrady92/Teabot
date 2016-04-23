from unittest import TestCase
from unittest import main
from status_helpers import get_is_teapot_full, get_teapot_status
from mock import patch


class TestStatusHelpers(TestCase):

    def test_get_is_teapot_full_in_middle(self):
        self.assertTrue(get_is_teapot_full(3200, 3200, 250))

    def test_get_is_teapot_full_lower_bound(self):
        self.assertTrue(get_is_teapot_full(3200, 2950, 250))

    def test_get_is_teapot_full_upper_bound(self):
        self.assertTrue(get_is_teapot_full(3200, 3450, 250))

    def test_get_is_teapot_full_below_lower_bound(self):
        self.assertFalse(get_is_teapot_full(3200, 2949, 250))


if __name__ == '__main__':
    main()
