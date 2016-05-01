from unittest import TestCase
from unittest import main
from mock import patch, Mock
from datetime import datetime
from kinda_idempotent_sender import KindaIdempotentSender


class TestKindaIdempotentSender(TestCase):

    def test_first_use_should_send(self):
        sender = KindaIdempotentSender(20)
        send_fn = Mock()
        sender.send(send_fn)
        send_fn.assert_called_once()

    @patch("kinda_idempotent_sender.KindaIdempotentSender._get_current_time")
    def test_two_calls_before_expiry_period(self, mock_get_time):
        mock_get_time.side_effect = iter([
            datetime(2016, 04, 04, 12, 00, 00),
            datetime(2016, 04, 04, 12, 01, 00)
        ])
        sender = KindaIdempotentSender(20)
        send_fn = Mock()

        result = sender.send(send_fn)
        send_fn.assert_called_once()
        self.assertTrue(result)

        result = sender.send(send_fn)
        send_fn.assert_called_once()
        self.assertFalse(result)

    @patch("kinda_idempotent_sender.KindaIdempotentSender._get_current_time")
    def test_two_calls_after_expiry_period(self, mock_get_time):
        mock_get_time.side_effect = iter([
            datetime(2016, 04, 04, 12, 00, 00),
            datetime(2016, 04, 04, 12, 21, 00),
            datetime(2016, 04, 04, 12, 21, 00)
        ])
        sender = KindaIdempotentSender(20)
        send_fn = Mock()

        result = sender.send(send_fn)
        self.assertTrue(result)
        send_fn.assert_called_once()

        result = sender.send(send_fn)
        self.assertEqual(send_fn.call_count, 2)
        self.assertTrue(result)

    @patch("kinda_idempotent_sender.KindaIdempotentSender._get_current_time")
    def test_three_calls(self, mock_get_time):
        mock_get_time.side_effect = iter([
            datetime(2016, 04, 04, 12, 00, 00),
            datetime(2016, 04, 04, 12, 21, 00),
            datetime(2016, 04, 04, 12, 21, 10),
            datetime(2016, 04, 04, 12, 22, 00)
        ])
        sender = KindaIdempotentSender(20)

        send_fn = Mock()
        result = sender.send(send_fn)
        self.assertTrue(result)
        send_fn.assert_called_once()

        result = sender.send(send_fn)
        self.assertEqual(send_fn.call_count, 2)
        self.assertTrue(result)

        result = sender.send(send_fn)
        self.assertEqual(send_fn.call_count, 2)
        self.assertFalse(result)


if __name__ == '__main__':
    main()
