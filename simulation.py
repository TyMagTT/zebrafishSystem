from components import Tank, Meter, Regulator, Controller
from settings_reader import open_file, create_components
from time import sleep

my_parameters = open_file('starting_parameters.json')
my_settings = open_file('parameter_settings.json')
tanks, meters, regulators, other = create_components('component_settings.json', my_parameters)
controller = Controller(tanks, meters, regulators, other, my_settings)


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
        tank_name = f'Tank{id(tank)}'
        formatted = f'{type} of {tank_name} is {value} {unit} ({arrow})'
        print(formatted)
    print('\n')


for i in range(180):
    for tank in tanks:
        tank.simulate()
    controller.step()
    print_current_values(meters)

    sleep(1)
