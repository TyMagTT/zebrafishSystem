from components import Meter, Tank

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
