import requests
from constants import TeapotStatuses, Constants
from datetime import datetime, timedelta


class ServerCommunicator(object):

    def __init__(self):
        self.endpoint_base = ""
        self.next_send_time = None
        self.constants = Constants()

    def send_status_update(self, status, timestamp, number_of_cups_remaining):
        if status == TeapotStatuses.FULL_TEAPOT:
            self._queue_brewed_update()

        requests.post(
            self.constants.get_endpoint_base_url(),
            data={
                "state": status,
                "timestamp": timestamp,
                "num_of_cups": number_of_cups_remaining
            }
        )

    def _queue_brewed_update(self):
        self.next_send_time = self._get_current_time() + \
            timedelta(minutes=self.constants.get_brew_delay_minutes())

    def _get_current_time(self):
        return datetime.now()

    def send_queued_update_if_time(self):
        if not self.next_send_time:
            return False
        if self._get_current_time() < self.next_send_time:
            return False
        requests.post(
            self.constants.get_endpoint_base_url() + "teaReady",
        )
        self.next_send_time = None
        return True
