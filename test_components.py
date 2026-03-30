from components import Meter, Tank, Regulator, Controller
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
        "high_value": 29,
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


def test_controller_check_parameter():
    test_parameters = [
        {
            "id": "ph",
            "value": 6.25,
            "simulation": {
                "average_change": 0.05
            }
        }
    ]
    my_tank = Tank(test_parameters)
    my_meter = Meter(my_tank, "ph", 6.25, "pH")
    my_pump = Regulator(my_tank, "ph", 0.5)
    my_controller = Controller([my_meter], [my_pump], [], my_settings)
    assert my_controller.check_parameter("ph") == "alarm_low"  # 6.25
    my_pump.work()
    my_meter.update_value()
    assert my_controller.check_parameter("ph") == "low"  # 6.75
    my_pump.work()
    my_meter.update_value()
    assert my_controller.check_parameter("ph") == "normal"  # 7.25
    my_pump.work()
    my_pump.work()
    my_meter.update_value()
    assert my_controller.check_parameter("ph") == "high"  # 8.25
    my_pump.work()
    my_meter.update_value()
    assert my_controller.check_parameter("ph") == "alarm_high"  # 8.75
