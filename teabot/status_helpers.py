from __future__ import division
from collections import namedtuple
from datetime import datetime
from constants import Constants
from teapot_state import get_teapot_state_machine


class TeapotStatus(object):
    """Controls the change of states in the teapot state machine based on
    the environmental parameters passed into get_teapot_status
    """

    def __init__(self):
        self.configuration_constants = Constants()
        # Initially set to the oldest value possible so the first full teapot
        # is always full
        self.last_full_teapot_time = datetime.min

    def get_teapot_descriptor(self, teapot_status, number_of_cups_remaining):
        """Returns a named tuple representing the status of the teapot,
        essentially a class of getters with the status and number of cups
        remaining with a timestamp added for analytics purposes.

        Args:
            teapot_status (string) - Status of the teapot from the constants
                file
            number_of_cups_remaining (int) - Number of cups of tea remaining in
                the teapot
        Returns:
            NamedTuple containing the data passed in and the current timestamp
        """
        teapot_state = namedtuple(
            "teapot_status",
            ["teapot_state", "timestamp", "number_of_cups_remaining"]
        )
        return teapot_state(
            teapot_state=teapot_status,
            timestamp=datetime.utcnow(),
            number_of_cups_remaining=number_of_cups_remaining
        )

    def teapot_is_full(self, teapot_weight):
        """As people will never put exactly the same amount of water in the
        teapot we allow for one cup of teas tollerance between the constant we
        determined for the weight of a full teapot and the weight at which we
        determine the teapot to be full.

        Args:
            teapot_weight (int) - The current weight of the teapot
        Returns:
            Boolean - True if weight of the tea in the teapot is within
                one cups worth of tea of the full teapot weight
        """
        weight_of_tea_in_pot = self.get_weight_of_tea_in_pot(teapot_weight)
        return weight_of_tea_in_pot >= \
            self.configuration_constants.get_lower_bound_for_full_teapot()

    def teapot_is_cold(self, teapot_temperature):
        """Determines if the tea in the teapot is cold based on the current
        temperature being below a predetermined threshold

        Args:
            teapot_temperature (int) - Current temperature of the teapot
        Returns:
            Boolean - True if the teapot is cold, False otherwise
        """
        return teapot_temperature <= \
            self.configuration_constants.get_cold_teapot_temperature()

    def teapot_is_empty(self, teapot_weight):
        """Determines if there is any tea left in the teapot based on the
        weight of the tea in the pot being greater than nothing on the scale
        and less than or equal to the weight of an empty pot

        Args:
            teapot_weight (int) - The current weight of the teapot
        Returns
            Boolean - True if the teapot is empty, False otherwise
        """
        zero_weight = self.configuration_constants.get_zero_weight()
        empty_weight = self.configuration_constants.get_empty_teapot_weight()
        return teapot_weight <= empty_weight and teapot_weight > zero_weight

    def scale_is_empty(self, teapot_weight):
        """Determines if there is nothing on the scales currently based on the
        weight being less than or equal to a predetermined threshold

        Args:
            teapot_weight (int) - The current weight of the teapot
        Returns
            Boolean - True if there is no teapot on the scale, False otherwise
        """
        zero_weight = self.configuration_constants.get_zero_weight()
        return teapot_weight <= zero_weight

    def get_weight_of_tea_in_pot(self, teapot_weight):
        """Returns the weight of the tea in the pot. Hides any issues with
        this method being called when the teapot has been lifted from the
        scales by never returning a value below 0

        Args:
            teapot_weight - The current weight of the teapot
        Returns:
            Int - Weight of the tea in the pot
        """
        empty_teapot_weight = \
            self.configuration_constants.get_empty_teapot_weight()
        return max((teapot_weight - empty_teapot_weight), 0)

    def calculate_number_of_cups_remaining(self, teapot_weight):
        """Determines the number of cups of tea left in the pot. Anything
        greater than or equal to half a cup is rounded up to a full cup
        anything less is rounded down.

        Args:
            teapot_weight - Weight of the teapot
        Returns
            Int - Number of cups of tea left in the pot
        """
        weight_of_tea_in_cup = \
            self.configuration_constants.get_weight_of_tea_in_cup()
        tea_weight = self.get_weight_of_tea_in_pot(teapot_weight)
        print "exact number of cups left", tea_weight / weight_of_tea_in_cup
        return int(round(tea_weight / weight_of_tea_in_cup))

    def get_current_time(self):
        """Wrapper around datetime.utcnow() so that we can mock it in testing"""
        return datetime.utcnow()

    def new_teapot_is_not_duplicate(self):
        """Determines if enough time has passed since the last full teapot that
        this one could be a new one.

        Args:
            -
        Returns:
            - True if this teapot is not a duplicate new teapot false otherwise
        """
        refresh_time = self.last_full_teapot_time + \
            self.configuration_constants.get_new_teapot_refresh_period()
        current_time = self.get_current_time()
        if current_time >= refresh_time:
            self.last_full_teapot_time = current_time
            return True
        return False

    def get_teapot_status(
            self, teapot_weight, teapot_temperature,
            teapot_temperature_is_rising_or_constant):
        """Determines the current status of the teapot using a finite state
        machine to transform the previous state of the teapot to the new state
        based on the readings from the sensors.

        Args:
            teapot_weight (int) - Current weight of the teapot
            teapot_temperature (int) - Current temperature of the teapot
            teapot_temperature_is_rising_or_constant (boolean) - If the
                temperature is currently rising or constant
        Returns
            A namedtuple describing the state of the status (see
            get_teapot_descriptor)
        """
        state_machine = get_teapot_state_machine()
        teapot_full = self.teapot_is_full(teapot_weight)
        teapot_cold = self.teapot_is_cold(teapot_temperature)
        teapot_empty = self.teapot_is_empty(teapot_weight)
        scale_empty = self.scale_is_empty(teapot_weight)

        print "###############"
        print "teapot full", teapot_full
        print "teapot_cold", teapot_cold
        print "teapot_empty", teapot_empty
        print "scale_empty", scale_empty
        print "temp_rising_or_constant", \
            teapot_temperature_is_rising_or_constant

        new_status = None
        print "state at start is", state_machine.current
        # This condition and (not teapot_empty and not teapot_full) are not
        # mutually exclusive if the scales are empty teapot_empty returns
        # False as does teapot_full.
        # Scales empty checks for the weight being basically 0 though and the
        # teapot_empty check is stricter so we should be able to just check for
        # scale empty first.
        if scale_empty:
            new_status = state_machine.current
        elif teapot_temperature_is_rising_or_constant and teapot_full:
            if self.new_teapot_is_not_duplicate():
                state_machine.temp_rising_weight_above_full()
            else:
                # This makes the teapot state be GOOD_TEAPOT and we don't
                # have to worry about duplicate new teapot alerts
                state_machine.weight_above_empty_below_full()
            new_status = state_machine.current
        elif not teapot_empty and not teapot_full and not teapot_cold:
            state_machine.weight_above_empty_below_full()
            new_status = state_machine.current
        elif teapot_cold and not teapot_empty:
            state_machine.temp_below_cold_weight_above_empty()
            new_status = state_machine.current
        elif teapot_cold and not teapot_empty:
            state_machine.temp_below_cold()
            new_status = state_machine.current
        elif teapot_empty:
            state_machine.weight_below_empty()
            new_status = state_machine.current
        else:
            raise Exception("None of the expected conditions were satisfied")

        number_of_cups = self.calculate_number_of_cups_remaining(teapot_weight)
        return self.get_teapot_descriptor(new_status, number_of_cups)
