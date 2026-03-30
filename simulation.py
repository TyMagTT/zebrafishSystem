from components import Tank, Meter, Regulator, Controller
from time import sleep

my_parameters = [
    {
        "id": "ph",
        "value": 7.5,
        "simulation": {
            "average_change": 0.05
        }
    },
    {
        "id": "temperature",
        "value": 27,
        "simulation": {
            "average_change": 0.1
        }
    },
    {
        "id": "conductivity",
        "value": 700,
        "simulation": {
            "average_change": 5
        }
    }
]

my_settings = [
    {
        "id": "ph",
        "alarm_low": 6.5,
        "low_value": 7.0,
        "high_value": 8.0,
        "alarm_high": 8.5
    },
    {
        "id": "temperature",
        "alarm_low": 23,
        "low_value": 25,
        "high_value": 28,
        "alarm_high": 30
    },
    {
        "id": "conductivity",
        "alarm_low": 500,
        "low_value": 650,
        "high_value": 750,
        "alarm_high": 1000
    }
]

my_tank = Tank(my_parameters)
ph_meter = Meter(my_tank, "ph", 0, "pH")
temp_meter = Meter(my_tank, "temperature", 0, "pH")
conduct_meter = Meter(my_tank, "conductivity", 0, "pH")
ph_pump = Regulator(my_tank, "ph", 0.1)
heater = Regulator(my_tank, "temperature", 0.2)
water_pump = Regulator(my_tank, "conductivity", 10)

meters = [ph_meter, temp_meter, conduct_meter]
pumps = [ph_pump, heater, water_pump]

controller = Controller([my_tank], meters, pumps, [], my_settings)

for i in range(180):
    if ph_meter.is_raising:
        ph_arrow = "↑"
    else:
        ph_arrow = "↓"

    if temp_meter.is_raising:
        temp_arrow = "↑"
    else:
        temp_arrow = "↓"

    if conduct_meter.is_raising:
        con_arrow = "↑"
    else:
        con_arrow = "↓"

    ph_string = f'Current ph is {round(my_tank.check("ph"), 2)} {ph_arrow}'
    temp_string = f'Current temp is {round(my_tank.check("temperature"), 2)} {temp_arrow}'
    conduct_string = f'Current conduct is {round(my_tank.check("conductivity"), 2)} {con_arrow}\n'
    print(ph_string)
    print(temp_string)
    print(conduct_string)
    my_tank.simulate()
    controller.step()
    sleep(1)
