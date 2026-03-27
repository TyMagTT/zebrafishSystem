from components import Tank
from time import sleep

my_parameters = [
    {
        "id": "ph",
        "value": 7.5,
        "simulation": {
            "average_change": 0.01
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

my_tank = Tank(my_parameters)

for i in range(60):
    ph_string = f'Current ph is {my_tank.check("ph")}'
    temp_string = f'Current temp is {my_tank.check("temperature")}'
    conduct_string = f'Current conduct is {my_tank.check("conductivity")}\n'
    print(ph_string)
    print(temp_string)
    print(conduct_string)
    my_tank.simulate()
    sleep(1)
