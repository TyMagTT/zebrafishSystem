from settings_reader import open_file, create_components

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

component_settings = [
    {
        "meters": [
            "ph",
            "temperature",
            "conductivity"
        ],
        "regulators": [
            "ph",
            "temperature",
            "conductivity"
        ],
        "other": [
            "lights"
        ]
    }
]


def test_open_file():
    file = open_file("starting_parameters.json")
    assert file == starting_parameters


def test_open_file2():
    file = open_file("parameter_settings.json")
    assert file == parameter_settings
