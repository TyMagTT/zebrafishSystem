import json
from os.path import splitext
from copy import deepcopy
from components import Meter, Regulator, Tank


def open_file(path):
    extension = splitext(path)[1]
    if extension != '.json':
        raise ValueError
    with open(path) as file_handle:
        setting_list = json.load(file_handle)
    return setting_list


def create_components(path, tank_settings):
    component_list = open_file(path)
    tank_list = []
    meter_list = []
    regulator_list = []
    other_list = []
    for tank in component_list:
        tank_object = Tank(deepcopy(tank_settings))
        for id in tank['meters']:
            unit = tank['meters'][id]
            new_meter = Meter(tank_object, id, 0, unit)
            meter_list.append(new_meter)
        for id in tank['regulators']:
            speed = tank['regulators'][id]
            new_regulator = Regulator(tank_object, id, speed)
            regulator_list.append(new_regulator)
        for other in tank['other']:
            pass
        tank_list.append(tank_object)
    return tank_list, meter_list, regulator_list, other_list
