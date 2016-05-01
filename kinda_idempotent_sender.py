from datetime import datetime, timedelta


class KindaIdempotentSender(object):

    def __init__(self, reset_period):
        self.reset_period = reset_period
        self.last_sent_at = None

    def _get_current_time(self):
        return datetime.now()

    def send(self, send_fn):
        if self.last_sent_at:
            current_time = self._get_current_time()
            expiry_time = self.last_sent_at + timedelta(
                minutes=self.reset_period)
            if current_time <= expiry_time:
                return False
        self.last_sent_at = self._get_current_time()
        send_fn()
        return True
