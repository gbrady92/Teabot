from Scale import Scale
from status_helpers import get_teapot_status

scale = Scale()

while True:
    weight = scale.get_scale_reading()
    print weight
    status = get_teapot_status(
        temperature=50, weight=weight, new_teapot_temperature=50,
        new_teapot_weight=60, empty_teapot_weight=0, cold_teapot_temperature=20)
    print status
