# LIBRARIES

from components import Controller
from settings_reader import open_file, create_components
from time import sleep
from math import floor
from matplotlib import pyplot as plt


# FILES

my_parameters = open_file('starting_parameters.json')
my_settings = open_file('parameter_settings.json')
language_file = open_file('language.json')
tanks, meters, regulators, other = create_components('component_settings.json', my_parameters)
controller = None


# FUNCTIONS

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


def create_graph(frame_number, saved_values, msg):
    plot_seconds = list(range(0, frame_number))
    for meter in saved_values:
        if meter[-2:] == 'ph':
            plot_values(0, plot_seconds, saved_values[meter], msg['ph'], msg['steps'], msg['unit'])
        elif meter[-2:] == 're':
            plot_values(1, plot_seconds, saved_values[meter], msg['ph'], msg['steps'], msg['unit'])
        elif meter[-2:] == 'ty':
            plot_values(2, plot_seconds, saved_values[meter], msg['ph'], msg['steps'], msg['unit'])
    plt.show()


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
            return languages[answer]
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


def next_state(state, command):
    match state:
        case 0:
            if command == 'run':
                return 1
            if command == 'edit':
                return 5
            if command == 'exit':
                return -1
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
            if command == 'no':
                return 40
            if command == 'yes':
                return 41
        case 5:
            if command == 'controller':
                return 8
            if command == 'back':
                return 0
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
        case 40:
            return 0
        case 41:
            return 0
        case 60:
            return 6
        case 61:
            return 6
        case 62:
            return 6
        case 70:
            return 7
        case 71:
            return 7
        case 72:
            return 7
        case 80:
            if command == 'alarm_low':
                return 800
            if command == 'low_value':
                return 801
            if command == 'high_value':
                return 802
            if command == 'alarm_high':
                return 803
            if command == 'back':
                return 8
        case 81:
            if command == 'alarm_low':
                return 810
            if command == 'low_value':
                return 811
            if command == 'high_value':
                return 812
            if command == 'alarm_high':
                return 813
            if command == 'back':
                return 8
        case 82:
            if command == 'alarm_low':
                return 820
            if command == 'low_value':
                return 821
            if command == 'high_value':
                return 822
            if command == 'alarm_high':
                return 823
            if command == 'back':
                return 8
    if state >= 500 and state < 600:
        if command == 'simulation':
            return 6
        if command == 'components':
            return 7
    if state >= 800 and state < 900:
        return 8
    raise ValueError


def execute_state(state):
    match state:
        case -1:
            message = f'\n{msg['exit']}'
            quit(message)
        case 0:
            command = select_option(msg['select_mode'], msg['again'], ['run', 'edit', 'exit'])
            data = None
            return command, data
        case 1:
            command = None
            number = False
            while not number:
                message = f'{msg['select_duration']}\n'
                data = input(message)
                try:
                    data = int(data)
                    number = True
                except ValueError:
                    print(msg['again'])
            return command, data
        case 2:
            command = select_option(msg['begin'], msg['again'], ['begin', 'back'])
            data = None
            return command, data
        case 3:
            command = None
            controller = Controller(tanks, meters, regulators, other, my_settings)
            data = simulate(tanks, meters, controller, frame_number, wait_time)
            return command, data
        case 4:
            create_graph(frame_number, saved_values, msg)
            command = select_option(msg['save_graph'], msg['again'], ['no', 'yes'])
            data = None
            return command, data
        case 5:
            command = select_option(msg['edit_param'], msg['again'], ['controller', 'back'])
            data = None
            return command, data
        case 6:
            command = None
            data = None
            return command, data
        case 7:
            command = None
            data = None
            return command, data
        case 8:
            for type in my_settings:
                id = type['id']
                alarm_low = type['alarm_low']
                low_value = type['low_value']
                high_value = type['high_value']
                alarm_high = type['alarm_high']
                print(f'\n{id}:')
                print(f'alarm_low: {alarm_low}')
                print(f'low_value: {low_value}')
                print(f'high_value: {high_value}')
                print(f'alarm_high: {alarm_high}')
            command = select_option(msg['edit_param'], msg['again'], ['ph', 'temp', 'conduct', 'back'])
            data = None
            return command, data
        case 40:
            command = None
            data = None
            return command, data
        case 41:
            command = None
            data = None
            return command, data
        case 60:
            command = None
            data = None
            return command, data
        case 61:
            command = None
            data = None
            return command, data
        case 62:
            command = None
            data = None
            return command, data
        case 70:
            command = None
            data = None
            return command, data
        case 71:
            command = None
            data = None
            return command, data
        case 72:
            command = None
            data = None
            return command, data
        case 80:
            command = select_option(msg['choose_point'], ['again'], ['alarm_low', 'low_value', 'high_value', 'alarm_high', 'back'])
            data = None
            return command, data
        case 81:
            command = select_option(msg['choose_point'], ['again'], ['alarm_low', 'low_value', 'high_value', 'alarm_high', 'back'])
            data = None
            return command, data
        case 82:
            command = select_option(msg['choose_point'], ['again'], ['alarm_low', 'low_value', 'high_value', 'alarm_high', 'back'])
            data = None
            return command, data
        case 600:
            command = None
            data = None
            return command, data
        case 601:
            command = None
            data = None
            return command, data
        case 602:
            command = None
            data = None
            return command, data
        case 603:
            command = None
            data = None
            return command, data
        case 610:
            command = None
            data = None
            return command, data
        case 611:
            command = None
            data = None
            return command, data
        case 612:
            command = None
            data = None
            return command, data
        case 613:
            command = None
            data = None
            return command, data
        case 620:
            command = None
            data = None
            return command, data
        case 621:
            command = None
            data = None
            return command, data
        case 622:
            command = None
            data = None
            return command, data
        case 623:
            command = None
            data = None
            return command, data
        case 700:
            command = None
            data = None
            return command, data
        case 701:
            command = None
            data = None
            return command, data
        case 710:
            command = None
            data = None
            return command, data
        case 711:
            command = None
            data = None
            return command, data
        case 720:
            command = None
            data = None
            return command, data
        case 721:
            command = None
            data = None
            return command, data
        case 800:
            command = None
            number = False
            while not number:
                message = f'{msg['new_value']}\n'
                data = input(message)
                try:
                    data = float(data)
                    data = round(data, 3)
                    number = True
                except ValueError:
                    print(msg['again'])
            return command, data
        case 801:
            command = None
            data = None
            return command, data
        case 802:
            command = None
            data = None
            return command, data
        case 803:
            command = None
            data = None
            return command, data
        case 810:
            command = None
            data = None
            return command, data
        case 811:
            command = None
            data = None
            return command, data
        case 812:
            command = None
            data = None
            return command, data
        case 813:
            command = None
            data = None
            return command, data
        case 820:
            command = None
            data = None
            return command, data
        case 821:
            command = None
            data = None
            return command, data
        case 822:
            command = None
            data = None
            return command, data
        case 823:
            command = None
            data = None
            return command, data
    raise ValueError


# SIMULATION

msg = select_language(language_file)
state = 0
frame_number = 0
wait_time = 0.001
saved_values = {}
fig, ax = plt.subplots(3, 1)
on = True

while on:
    command, data = execute_state(state)
    if state == 1:
        second_duration = data
        frame_number = floor(second_duration / wait_time)
    elif state == 3:
        saved_values = data
    elif state >= 800 and state < 900:
        state_string = str(state)
        state_numbers = list(state_string)
        if state_numbers[1] == '0':
            param = 'ph'
        elif state_numbers[1] == '1':
            param = 'temperature'
        elif state_numbers[1] == '2':
            param = 'conductivity'
        if state_numbers[2] == '0':
            value = 'alarm_low'
        elif state_numbers[2] == '1':
            value = 'low_value'
        elif state_numbers[2] == '2':
            value = 'high_value'
        elif state_numbers[2] == '3':
            value = 'alarm_high'
        for setting in my_settings:
            if setting['id'] == param:
                setting[value] = data
    state = next_state(state, command)
