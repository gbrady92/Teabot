import os
import glob
import time
from itertools import tee


class Temperature(object):
    """Controls interactions with the Temperature sensor"""

    def __init__(self):
        # Initialize the GPIO Pins
        os.system('modprobe w1-gpio')  # Turns on the GPIO module
        os.system('modprobe w1-therm')  # Turns on the Temperature module

        # Finds the correct device file that holds the temperature data
        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '28*')[0]
        self.device_file = device_folder + '/w1_slave'

    # A function that reads the sensors data
    def read_temp_raw(self):
        f = open(self.device_file, 'r')  # Opens the temperature device file
        lines = f.readlines()  # Returns the text
        f.close()
        return lines

    # Convert the value of the sensor into a temperature
    def get_reading(self):
        lines = self.read_temp_raw()  # Read the temperature 'device file'

        # While the first line does not contain 'YES', wait for 0.2s
        # and then read the device file again.
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_temp_raw()

        # Look for the position of the '=' in the second line of the
        # device file.
        equals_pos = lines[1].find('t=')

        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2:]
            temp_c = float(temp_string) / 1000.0
            return temp_c

    def is_rising_or_constant(self):
        """Used to determine if the temperature being read is increasing or
        constant. By polling the sensor 10 times and analysing the output

        Returns:
            Boolean - True if the majority of the 10 readings obtained are
            increasing or the same
        """
        set_of_readings = [self.get_reading() for _ in range(0, 10)]
        number_rising = 0
        number_falling = 0
        for x, y in self.pairwise(set_of_readings):
            if y >= x:
                number_rising += 1
            else:
                number_falling += 1
        if number_rising > number_falling:
            return True
        return False

    def pairwise(self, iterable):
        """From the itertools recipes takes an iterable and returns overlapping
        pairs e.g.
            s -> (s0,s1), (s1,s2), (s2, s3), ...

        Returns:
            Iterable
        """
        a, b = tee(iterable)
        next(b, None)
        return zip(a, b)
