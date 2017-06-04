import requests
from teabot.constants import TeapotStatuses, Constants
from datetime import datetime, timedelta
import json


class ServerCommunicator(object):
    """Controls interacts with the REST endpoints, posting updates about
    the state of the teapot to the server
    """

    def __init__(self):
        self.next_send_time = None
        self.constants = Constants()

    def send_status_update(
            self, status, timestamp, number_of_cups_remaining, weight,
            temperature):
        """Sends the state of the teapot to the server and if this is a
        FULL_TEAPOT schedules an alert to be sent out (via the server)
        announcing that a new teapot is ready

        Args:
            status (string) - State of the teapot
            timestamp (datetime) - Time this status happened
            number_of_cups_remaining (int) - Number of cups of tea left in the
                pot
        Returns
            None
        """
        if status == TeapotStatuses.FULL_TEAPOT:
            self._queue_brewed_update()

        requests.post(
            self.constants.get_endpoint_base_url() + "storeState",
            data=json.dumps({
                "state": status,
                "timestamp": timestamp.isoformat(),
                "num_of_cups": number_of_cups_remaining,
                "weight": weight,
                "temperature": temperature
            })
        )

    def _queue_brewed_update(self):
        """Schedules an alert to be sent out about a brewed teapot by setting
        next_send_time, this value is checked by the send_queued_update_if_time
        function and if the current time exceeds this an brewed alert is sent.
        """
        self.next_send_time = self._get_current_time() + \
            timedelta(minutes=self.constants.get_brew_delay_minutes())

    def _get_current_time(self):
        """Wrapper for datetime.utcnow() as it can't be mocked in testing"""
        return datetime.utcnow()

    def send_queued_update_if_time(self):
        """Sends an alert that a new teapot has brewed if it is time. This
        function is designed to be called repeatedly after an alert has been
        queued.

        Returns:
            Boolean - True if a brewed alert was sent, False otherwise
        """
        if not self.next_send_time:
            return False
        if self._get_current_time() < self.next_send_time:
            return False
        requests.post(
            self.constants.get_endpoint_base_url() + "teaReady"
        )
        self.next_send_time = None
        return True

    def send_flip_teapot_request(self, dash_mac_address):
        """Calls endpoint to flip teapot request if dash button click is detected

        Args:
            dash_mac_address - str - Dash button mac dash_mac_address

        Returns:
            None
        """

        requests.post(
            self.constants.get_endpoint_base_url() + "flipTeapotRequest",
            data=json.dumps({"dash_mac_address": dash_mac_address}))
