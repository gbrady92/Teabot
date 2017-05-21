from datetime import datetime, timedelta
from itertools import tee
import time


class BaseSensor(object):
    POLL_PERIOD = timedelta(seconds=1)
    MAX_AGE = timedelta(minutes=10)

    def __init__(self):
        self.recent_readings = []

    def prune_readings(self):
        oldest_allowed = datetime.now() - self.MAX_AGE
        first_valid_index = None
        for i, reading in enumerate(self.recent_readings):
            if reading['ts'] >= oldest_allowed:
                first_valid_index = i
                break

        if first_valid_index:
            print "pruning readings", i, self.recent_readings
            self.recent_readings = self.recent_readings[first_valid_index:]

    def get_reading(self):
        raise NotImplementedError(
            "Please implement get_reading() for %s." % self.__class__)

    def get_readings(self, from_dt=None, to_dt=None, wait=False):
        """Update recent_readings; Get readings between from_dt and to_dt."""
        now = datetime.now()

        if not self.recent_readings \
                or self.recent_readings[-1]['ts'] < now - self.POLL_PERIOD:
            reading = self.get_reading()
            self.recent_readings.append({'ts': now, 'reading': reading})
            self.prune_readings()
        elif wait:
            pause = self.recent_readings[-1]['ts'] + self.POLL_PERIOD - now
            time.sleep(pause.total_seconds())
            # recurse once
            return self.get_readings(from_dt, to_dt)

        if from_dt is None and to_dt is None:
            return self.recent_readings

        first_index = 0
        last_index = 0
        for i, reading in enumerate(self.recent_readings):
            if from_dt is None or reading['ts'] >= from_dt:
                first_index = i
            if to_dt is None or reading['ts'] <= to_dt:
                last_index = i + 1

        return self.recent_readings[first_index:last_index]

    def is_rising_or_constant(self):
        """Used to determine if the sensor being read is increasing or
        constant. By polling the sensor 10 times and analysing the output

        TODO: make it take a timedelta, so it's easier to reason about?
        TODO: just check whether set_of_readings[0] < set_of_readings[-1]?

        Returns:
            Boolean - True if the majority of the 10 readings obtained are
            increasing or the same
        """
        set_of_readings = []
        wait = False
        while len(set_of_readings) < 10:
            set_of_readings = [
                r['reading'] for r in self.get_readings(wait=wait)[-10:]]
            # if we need to go around the loop to get more, wait for them.
            wait = True

        number_rising = 0
        number_falling = 0
        for x, y in self._pairwise(set_of_readings):
            if y >= x:
                number_rising += 1
            else:
                number_falling += 1
        if number_rising > number_falling:
            return True
        return False

    def _pairwise(self, iterable):
        """From the itertools recipes takes an iterable and returns overlapping
        pairs e.g.
            s -> (s0,s1), (s1,s2), (s2, s3), ...

        Returns:
            Iterable
        """
        a, b = tee(iterable)
        next(b, None)
        return zip(a, b)
