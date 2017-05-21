import usb.core
import usb.util

from teabot.inputs.base import BaseSensor

VENDOR_ID = 0x0922
PRODUCT_ID = 0x8006


class Weight(BaseSensor):
    """Controls interactions with the scales"""

    def __init__(self):
        super(Weight, self).__init__()
        self.device = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

        if self.device.is_kernel_driver_active(0):
            self.device.detach_kernel_driver(0)
            # use the first/default configuration
            self.device.set_configuration()

    def most_common(self, list_of_readings):
        """Returns the most common value amongst the list of readings passed
        in.

        Args:
            list_of_readings (list) - List of readings obtained from the scales
        Returns:
            Float - most common reading in list
        """
        return max(list_of_readings, key=list_of_readings.count)

    def read_sensor(self):
        """Returns the weight of the item on the scales in grams, testing has
        found that old values may be returned from the scales so multiple
        readings are taken and the most common is returned.

        Returns:
            Float - Weight of item on scales in grams
        """
        read_list = []
        endpoint = self.device[0][(0, 0)][0]
        try:
            reads = 10
            while reads > 0:
                scale_data = self.device.read(
                    endpoint.bEndpointAddress,
                    endpoint.wMaxPacketSize)

                read_list.append(
                    scale_data[4] + (256 * scale_data[5]))
                reads -= 1
            data = self.most_common(read_list)
            return data
        except Exception:
                print "Exception reading value from scales, may be expected"
                return 0
