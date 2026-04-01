from components import Controller
from settings_reader import open_file, create_components
from time import sleep
from math import floor
from matplotlib import pyplot as plt


my_parameters = open_file('starting_parameters.json')
my_settings = open_file('parameter_settings.json')
tanks, meters, regulators, other = create_components('component_settings.json', my_parameters)
controller = Controller(tanks, meters, regulators, other, my_settings)


def format_tank_name(tank_object):
    return f'Tank{str(id(tank_object))[-3:]}'


def check_meters(meters):
    values = []
    for meter in meters:
        tank = meter.current_object()
        type = meter.type()
        value = meter.value()
        unit = meter.unit()
        working = meter.is_raising
        reading = (tank, type, value, unit, working)
        values.append(reading)
    return values


def print_current_values(meters):
    readings = check_meters(meters)
    for reading in readings:
        tank, type, value, unit, working = reading
        value = round(value, 2)
        arrow = "↑" if working else "↓"
        tank_name = format_tank_name(tank)
        formatted = f'{type} of {tank_name} is {value} {unit} ({arrow})'
        print(formatted)


def save_values(dictionary):
    readings = check_meters(meters)
    for reading in readings:
        tank, type, value, unit, working = reading
        tank_name = format_tank_name(tank)
        value = round(value, 2)
        meter_name = f'{tank_name}_{type}'
        if meter_name in dictionary.keys():
            dictionary[meter_name].append(value)
        else:
            dictionary[meter_name] = [value]


def plot_values(sub_x, x, y, title, x_label, y_label):
    ax[sub_x].plot(x, y)
    # ax[sub_x].set_ylim(bottom=0)
    ax[sub_x].set_title(title)
    ax[sub_x].set_xlabel(x_label)
    ax[sub_x].set_ylabel(y_label)


minute_duration = 0.03
wait_time = 0.001
frame_number = floor(minute_duration * 60 / wait_time)
plot_seconds = list(range(0, frame_number))
saved_values = {}

for i in range(frame_number):
    for tank in tanks:
        tank.simulate()
    controller.step()
    print_current_values(meters)
    save_values(saved_values)
    sleep(wait_time)

fig, ax = plt.subplots(3, 1)

for meter in saved_values:
    if meter[-2:] == 'ph':
        plot_values(0, plot_seconds, saved_values[meter], 'pH', 'Steps', 'Unit')
    elif meter[-2:] == 're':
        plot_values(1, plot_seconds, saved_values[meter], 'Temperature', 'Steps', 'Unit')
    elif meter[-2:] == 'ty':
        plot_values(2, plot_seconds, saved_values[meter], 'Water Conductivity', 'Steps', 'Unit')
plt.show()
