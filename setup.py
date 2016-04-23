from __future__ import division
from inputs.weight import Weight
from inputs.temperature import Temperature


weight_sensor = Weight()
tempature_sensor = Temperature()
data_list = []
global stored_data_dict
stored_data_dict = dict()


def get_average_reading(key):
    stored_data_dict[key] = weight_sensor.get_scale_reading()
    print stored_data_dict[key]

print (raw_input('Place empty teapot on scale and press enter.'))

get_average_reading('empty_teapot')

print (raw_input('Place empty cup on scale and press enter.'))

get_average_reading('empty_cup')

print (raw_input('Place full teapot on scale and press enter.'))

get_average_reading('full_teapot')

print (raw_input('Place full cup on scale and press enter.'))

get_average_reading('full_cup')

weight_of_tea = stored_data_dict['full_teapot'] \
 - stored_data_dict['empty_teapot']
weight_of_tea_in_cup = stored_data_dict['full_cup'] \
 - stored_data_dict['empty_cup']

for i in stored_data_dict.keys():
    print stored_data_dict[i]

print 'weight_of_tea', weight_of_tea
print 'weight_of_tea_in_cup', weight_of_tea_in_cup

num_of_cups = weight_of_tea / weight_of_tea_in_cup

print 'num_of_cups', num_of_cups
