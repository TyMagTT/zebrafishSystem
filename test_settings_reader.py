from settings_reader import open_file, create_components
import pytest

starting_parameters = [
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

parameter_settings = [
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


def test_open_file():
    file = open_file('starting_parameters.json')
    assert file == starting_parameters


def test_open_file2():
    file = open_file('parameter_settings.json')
    assert file == parameter_settings


def test_open_file_not_json():
    with pytest.raises(ValueError):
        open_file('parameter_settings.txt')


def test_create_components():
    settings = open_file('starting_parameters.json')
    path = 'component_settings.json'
    tanks, meters, regulators, other = create_components(path, settings)
    assert len(tanks) == 1
    assert len(meters) == 3
    assert len(regulators) == 3
    assert len(other) == 0
