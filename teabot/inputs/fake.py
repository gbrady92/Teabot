from datetime import datetime, timedelta
import json

from teabot.inputs.base import BaseSensor

_cached_reading = None
_already_read = set()
_clock_offset = timedelta()


class FakeSensor(BaseSensor):
    """A fake sensor that reads its values from a pipe.

    The data format is one json blob per line.
    """
    def __init__(self, key, pipe):
        super(FakeSensor, self).__init__()
        self.key = key
        self.pipe = pipe
        # initialise clock and first reading.
        self.read_sensor()

    def __str__(self):
        return "FakeSensor(%s)" % self.key

    def now(self):
        return datetime.now() + _clock_offset

    def read_sensor(self):
        global _cached_reading
        global _already_read
        global _clock_offset

        if _cached_reading and self.key not in _already_read:
            # each sensor should only read the same line once
            _already_read.add(self.key)
        else:
            line = self.pipe.readline()
            _cached_reading = json.loads(line)
            _already_read = set([self.key])
            _clock_offset += timedelta(
                seconds=_cached_reading.get('offset_seconds', 0))

        return _cached_reading[self.key]
