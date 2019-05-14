from unittest import TestCase
from unittest import main
from teabot.server_communicator import ServerCommunicator
from teabot.constants import TeapotStatuses
from mock import patch, Mock
from datetime import datetime
import json


class TestServerCommunicator(TestCase):

    @patch("teabot.server_communicator.requests.post", autospec=True)
    @patch(
        "teabot.server_communicator.ServerCommunicator._queue_brewed_update",
        autospec=True)
    @patch("teabot.server_communicator.Constants", autospec=True)
    def test_send_status_update_full_teapot(
            self, mock_constants, mock_queue, mock_post):
        mock_constants.return_value = Mock(
            get_endpoint_base_url=Mock(return_value="abc/")
        )
        server_communicator = ServerCommunicator()
        send_time = datetime.utcnow()
        server_communicator.send_status_update(
            TeapotStatuses.FULL_TEAPOT, send_time, 5, 200
        )
        mock_queue.assert_called_once_with(server_communicator)
        mock_post.assert_called_once_with(
            "abc/storeState",
            data=json.dumps({
                "state": TeapotStatuses.FULL_TEAPOT,
                "timestamp": send_time.isoformat(),
                "num_of_cups": 5,
                "weight": 200,
                "temperature": None
            })
        )

    @patch("teabot.server_communicator.requests.post", autospec=True)
    @patch(
        "teabot.server_communicator.ServerCommunicator._queue_brewed_update",
        autospec=True)
    @patch("teabot.server_communicator.Constants", autospec=True)
    def test_send_status_update_not_full_teapot(
            self, mock_constants, mock_queue, mock_post):
        mock_constants.return_value = Mock(
            get_endpoint_base_url=Mock(return_value="abc/")
        )
        server_communicator = ServerCommunicator()
        send_time = datetime.utcnow()
        server_communicator.send_status_update(
            TeapotStatuses.GOOD_TEAPOT, send_time, 5, 200
        )
        self.assertFalse(mock_queue.call_count)
        mock_post.assert_called_once_with(
            "abc/storeState",
            data=json.dumps({
                "state": TeapotStatuses.GOOD_TEAPOT,
                "timestamp": send_time.isoformat(),
                "num_of_cups": 5,
                "weight": 200,
                "temperature": None
            })
        )

    @patch("teabot.server_communicator.requests.post", autospec=True)
    @patch("teabot.server_communicator.Constants", autospec=True)
    @patch("teabot.server_communicator.ServerCommunicator._get_current_time",
           autospec=True)
    def test_send_queued_update_not_time_yet(
            self, mock_get_time, mock_constants, mock_post):
        mock_constants.return_value = Mock(
            get_endpoint_base_url=Mock(return_value="abc"),
            get_brew_delay_minutes=Mock(return_value=5)
        )
        mock_get_time.side_effect = iter([
            datetime(2016, 01, 01, 12, 00, 00),
            datetime(2016, 01, 01, 12, 01, 00)
        ])
        server_communicator = ServerCommunicator()
        server_communicator.send_status_update(
            TeapotStatuses.FULL_TEAPOT, datetime.utcnow(), 5, 200
        )
        result = server_communicator.send_queued_update_if_time()
        self.assertEqual(mock_post.call_count, 1)
        self.assertFalse(result)

    def test_send_queued_update_if_time_nothing_queued(self):
        server_communicator = ServerCommunicator()
        result = server_communicator.send_queued_update_if_time()
        self.assertFalse(result)

    @patch("teabot.server_communicator.requests.post", autospec=True)
    @patch("teabot.server_communicator.Constants", autospec=True)
    @patch("teabot.server_communicator.ServerCommunicator._get_current_time",
           autospec=True)
    def test_send_queued_update_time(
            self, mock_get_time, mock_constants, mock_post):
        mock_constants.return_value = Mock(
            get_endpoint_base_url=Mock(return_value="abc"),
            get_brew_delay_minutes=Mock(return_value=5)
        )
        mock_get_time.side_effect = iter([
            datetime(2016, 01, 01, 12, 00, 00),
            datetime(2016, 01, 01, 12, 06, 00)
        ])
        server_communicator = ServerCommunicator()
        server_communicator.send_status_update(
            TeapotStatuses.FULL_TEAPOT, datetime.utcnow(), 5, 200
        )
        result = server_communicator.send_queued_update_if_time()
        self.assertEqual(mock_post.call_count, 2)
        self.assertTrue(result)

        # Now successive calls should do nothing
        for _ in range(10):
            result = server_communicator.send_queued_update_if_time()
            self.assertEqual(mock_post.call_count, 2)
            self.assertFalse(result)


if __name__ == '__main__':
    main()
