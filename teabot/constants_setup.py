from __future__ import division
from inputs.weight import Weight


weight_sensor = Weight()
data_list = []
global stored_data_dict
stored_data_dict = dict()


def store_reading(key):
    stored_data_dict[key] = weight_sensor.get_reading()

print (raw_input('Place empty teapot on scale and press enter.'))

store_reading('empty_teapot')

print (raw_input('Place empty cup on scale and press enter.'))

store_reading('empty_cup')

print (raw_input('Place full teapot on scale and press enter.'))

store_reading('full_teapot')

print (raw_input('Place full cup on scale and press enter.'))

store_reading('full_cup')

weight_of_tea = stored_data_dict['full_teapot'] \
    - stored_data_dict['empty_teapot']
stored_data_dict['weight_of_tea_in_cup'] = stored_data_dict['full_cup'] \
    - stored_data_dict['empty_cup']

stored_data_dict['cold_tea_temp'] = 40

for i, j in stored_data_dict.iteritems():
    print i, j

print 'Setup Complete.'
