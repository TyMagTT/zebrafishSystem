from components import Meter, Tank
import pytest

my_parameters = [
    {
        "id": "ph",
        "value": 7.0
    },
    {
        "id": "temperature",
        "value": 20.0
    }
]


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
    assert my_meter.value() == 10.0
    my_meter.update_value()
    assert my_meter.value() == 20.0


def test_tank_create_invalid():
    with pytest.raises(ValueError):
        Tank("I am not a list")


def test_tank_check():
    my_tank = Tank(my_parameters)
    assert my_tank.check("ph") == 7


def test_tank_check_invalid():
    my_tank = Tank(my_parameters)
    with pytest.raises(KeyError):
        my_tank.check("humidity")
