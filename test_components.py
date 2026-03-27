from components import Meter, Tank, Regulator
import pytest

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


def around(value, target, epsilon=0.001):
    return abs(value - target) < epsilon


def test_meter_create():
    my_meter = Meter(None, "temperature", 20.0, "°C")
    assert my_meter.value() == 20.0
    assert my_meter.unit() == "°C"


def test_meter_create_invalid():
    with pytest.raises(ValueError):
        Meter(None, "temperature", None, 15)


def test_meter_update():
    my_tank = Tank(my_parameters)
    my_meter = Meter(my_tank, "temperature", 10.0, "°C")
    assert around(my_meter.value(), 10)
    my_meter.update_value()
    assert around(my_meter.value(), 27)


def test_tank_create_invalid():
    with pytest.raises(ValueError):
        Tank("I am not a list")


def test_tank_check():
    my_tank = Tank(my_parameters)
    assert around(my_tank.check("ph"), 7.5)


def test_tank_check_invalid():
    my_tank = Tank(my_parameters)
    with pytest.raises(KeyError):
        my_tank.check("humidity")


def test_tank_change_by():
    my_tank = Tank(my_parameters)
    assert around(my_tank.check("ph"), 7.5)
    my_tank.change_by("ph", 1.0)
    assert around(my_tank.check("ph"), 8.5)


def test_regulator_work():
    my_tank = Tank(my_parameters)
    my_pump = Regulator(my_tank, "ph", 0.25)
    assert around(my_tank.check("ph"), 7.5)
    my_pump.work()
    assert around(my_tank.check("ph"), 7.75)
    my_pump.work()
    assert around(my_tank.check("ph"), 8.0)
