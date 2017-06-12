import json

from teabot.inputs.base import BaseSensor


class FakeSensor(BaseSensor):
    """A fake sensor that reads its values from a pipe.

    The data format is one json blob per line.
    """
    def __init__(self, key, pipe):
        super(FakeSensor, self).__init__()
        self.key = key
        self.pipe = pipe

    def __str__(self):
        return "FakeSensor(%s)" % self.key

    def read_sensor(self):
        line = self.pipe.readline()
        return json.loads(line)[self.key]
