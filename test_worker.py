from unittest import TestCase
from unittest import main
from constants import TeapotStatuses
from mock import patch, Mock
from datetime import datetime
from worker import do_work

class TestWorker(TestCase):

    # Currently doesn't work due to not being able to mockout the usb
    # stuff in time :(
    @patch("worker.Weight")
    @patch("worker.Temperature")
    @patch("worker.ServerCommunicator")
    @patch("worker.TeapotStatus")
    @patch("usb.core")
    @patch("glob.glob")
    def test_worker(
            self, mock_glob, mock_usb, mock_teapot, mock_server, mock_temp,
            mock_weight):
        mock_teapot.return_value = Mock(
            get_teapot_status=Mock(return_value=Mock(
                teapot_state=TeapotStatuses.NO_TEAPOT,
                number_of_cups_remaining=4,
                timestamp=123
            ))
        )
        do_work()


if __name__ == '__main__':
    main()
