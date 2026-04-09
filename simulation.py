from components import Controller
from settings_reader import open_file, create_components
from time import sleep
from math import floor
from matplotlib import pyplot as plt


my_parameters = open_file('starting_parameters.json')
my_settings = open_file('parameter_settings.json')
language = open_file('language.json')
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


def simulate(tanks, meters, controller, frame_number, wait_time):
    saved_values = {}
    for i in range(frame_number):
        for tank in tanks:
            tank.simulate()
        controller.step()
        print_current_values(meters)
        save_values(saved_values)
        sleep(wait_time)
    return saved_values


def select_language(languages):
    selected = False
    codes = languages.keys()
    codes_message = 'avaliable languages:'
    for code in codes:
        codes_message = f'{codes_message} {code} ({languages[code]["name"]}),'
        language_message = f'Input language code, {codes_message}\n'
    while not selected:
        answer = input(language_message)
        if answer in codes:
            selected = True
            return answer
        else:
            print('Language not found! Try again')


def select_option(select_msg, again_msg, options):
    selected = False
    full_message = f'{select_msg} '
    for option in options:
        full_message = f'{full_message} {option},'
    while not selected:
        answer = input(f'{full_message}\n')
        if answer in options:
            selected = True
            return answer
        else:
            print(again_msg)


def set_state(current_state, command):
    match current_state:
        case 0:
            if command == 'run':
                return 1
            if command == 'edit':
                return 5
        case 1:
            return 2
        case 2:
            if command == 'begin':
                return 3
            if command == 'back':
                return 0
        case 3:
            return 4
        case 4:
            return 0
        case 5:
            pass  # multiple tanks ????
        case 6:
            if command == 'ph':
                return 60
            if command == 'temp':
                return 61
            if command == 'conduct':
                return 62
            if command == 'back':
                return 5
        case 7:
            if command == 'ph':
                return 70
            if command == 'temp':
                return 71
            if command == 'conduct':
                return 72
            if command == 'back':
                return 5
        case 8:
            if command == 'ph':
                return 80
            if command == 'temp':
                return 81
            if command == 'conduct':
                return 82
            if command == 'back':
                return 5
    if current_state >= 50 and current_state < 60:
        if command == 'simulation':
            return 6
        if command == 'components':
            return 7
    raise ValueError


language_code = select_language(language)
msg = language[language_code]
print(msg['test'])
sleep(3)
command = select_option(msg['select_mode'], msg['again'], ['run', 'settings'])
state = 0
last_state = 0

minute_duration = 0.03
wait_time = 0.001
frame_number = floor(minute_duration * 60 / wait_time)
plot_seconds = list(range(0, frame_number))
saved_values = simulate(tanks, meters, controller, frame_number, wait_time)
fig, ax = plt.subplots(3, 1)

for meter in saved_values:
    if meter[-2:] == 'ph':
        plot_values(0, plot_seconds, saved_values[meter], msg['ph'], msg['steps'], msg['unit'])
    elif meter[-2:] == 're':
        plot_values(1, plot_seconds, saved_values[meter], msg['ph'], msg['steps'], msg['unit'])
    elif meter[-2:] == 'ty':
        plot_values(2, plot_seconds, saved_values[meter], msg['ph'], msg['steps'], msg['unit'])
plt.show()
