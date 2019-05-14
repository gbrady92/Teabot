import sys
from datetime import timedelta

import rollbar

from teabot.status_helpers import TeapotStatus


if '--fake' in sys.argv:
    from teabot.inputs.fake import FakeSensor
    weight_sensor = FakeSensor(key='weight', pipe=sys.stdin)
else:
    from teabot.inputs.weight import Weight
    weight_sensor = Weight()


teapot_status = TeapotStatus()
rollbar.init("")


def dump_sensors():
    weight_readings = weight_sensor.get_readings()
    min_ts = weight_readings[0]['ts']
    max_ts = weight_readings[-1]['ts']

    filename = max_ts.isoformat() + '.input'
    print "saving input to", filename

    with open(filename, 'w') as dumpfile:
        dumpfile.write(
            '{"weight": null, "offset_seconds": -%s}\n'
            % (max_ts - min_ts).total_seconds())

        last_ts = min_ts
        while weight_readings:
            wi = weight_readings[0]
            now = weight_readings.pop(0)['ts']

            if (now - last_ts).total_seconds() > 0.5:
                dumpfile.write(
                    '{"weight": %s, "offset_seconds": %s}\n'
                    % (
                        wi['reading'],
                        (now - last_ts).total_seconds()),
                )
                last_ts = now

        for wi in weight_readings:
            dumpfile.write(
                '{"weight": %s, "extra": "weight"}' % (wi['reading'])
            )


def do_work():
    """This is the entry point for teabot, this function polls the sensors for
    their lastest readings and then updates the state machine based on them.

    If the state of the teapot changes or the number of cups remaining changes
    this information is posted to the server where it is stored for analytics
    and querying purposes.
    """
    current_weight = weight_sensor.read_and_store(wait=True)
    last_preparation_period = weight_sensor.last_period_matching(
        condition=teapot_status.scale_is_empty, duration=timedelta(seconds=10))

    teapot_status.get_teapot_status(current_weight, last_preparation_period)


if __name__ == "__main__":
    while True:
        try:
            do_work()
        except Exception as e:
            rollbar.report_exc_info()
            dump_sensors()
            raise
        except KeyboardInterrupt:
            dump_sensors()
            raise
