
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
    def __init__(self):
        pass


class Tank:
    def __init__(self, parameters):
        if not isinstance(parameters, list):
            raise ValueError
        for parameter in parameters:
            value = parameter["value"]
            if not isinstance(value, float):
                parameter["value"] = float(value)
        self._parameters = parameters

    def check(self, parameter_id):
        if not isinstance(parameter_id, str):
            raise ValueError
        for parameter in self._parameters:
            if parameter['id'] == parameter_id:
                return parameter['value']
        raise KeyError


class Controller:
    def __init__(self):
        pass
