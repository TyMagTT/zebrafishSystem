from random import uniform


class Meter:
    def __init__(self, current_object, meter_type, current_value, unit):
        if not isinstance(unit, str):
            raise ValueError
        self._object = current_object
        self._type = meter_type
        self._current_value = current_value
        self._unit = unit

    def update_value(self):
        new_value = self._object.check(self._type)
        self._current_value = new_value

    def value(self):
        return self._current_value

    def unit(self):
        return self._unit


class Regulator:
    def __init__(self, current_object, regulator_type, speed):
        self._object = current_object
        self._type = regulator_type
        self._speed = speed

    def work(self):
        speed = float(self._speed)
        self._object.change_by(self._type, speed)


class Tank:
    def __init__(self, parameters):
        if not isinstance(parameters, list):
            raise ValueError
        for parameter in parameters:
            value = parameter['value']
            if not isinstance(value, float):
                parameter['value'] = float(value)
        self._parameters = parameters

    def change_by(self, parameter_id, value):
        if not isinstance(parameter_id, str):
            raise ValueError
        if not isinstance(value, float):
            raise ValueError
        for parameter in self._parameters:
            if parameter['id'] == parameter_id:
                parameter['value'] += value
                return

    def check(self, parameter_id):
        if not isinstance(parameter_id, str):
            raise ValueError
        for parameter in self._parameters:
            if parameter['id'] == parameter_id:
                return parameter['value']
        raise KeyError

    def simulate(self):
        for parameter in self._parameters:
            simulation = parameter['simulation']
            average_change = simulation['average_change']
            min_change = average_change * 0.75
            max_change = average_change * 1.25
            random_change = uniform(min_change, max_change)
            parameter['value'] -= random_change


class Controller:
    def __init__(self):
        pass
