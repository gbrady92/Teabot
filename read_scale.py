import usb.core
import usb.util

VENDOR_ID = 0x0922
PRODUCT_ID = 0x8006


class Scale(object):

    def __init__(self):
        self.device = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

        if self.device.is_kernel_driver_active(0):
            self.device.detach_kernel_driver(0)
        # use the first/default configuration
            self.device.set_configuration()

    def most_common(self, lst):
        # Returns the most common value in the list
        return max(lst, key=lst.count)

    def get_scale_reading(self):
        """Multiple readings from the scale are used as old values may be returned from scale.
           Scale readings are converted into grams and appended to read list.
           The most common value in the list is returned.
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
                pass
