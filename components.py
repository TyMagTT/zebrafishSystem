from random import uniform, randrange, choice


class Meter:
    def __init__(self, current_object, meter_type, current_value, unit, error = None):
        if not isinstance(unit, str):
            raise ValueError
        self._object = current_object
        self._type = meter_type
        self._current_value = current_value
        self._unit = unit
        self.is_raising = False
        self._error = error

    def update_value(self):
        if self.error() == 'meter_broken':
            new_value = None
        else:
            new_value = self._object.check(self._type)
        self._current_value = new_value

    def value(self):
        return self._current_value

    def unit(self):
        return self._unit

    def type(self):
        return self._type

    def current_object(self):
        return self._object

    def error(self):
        return self._error


class Regulator:
    def __init__(self, current_object, regulator_type, speed, error = None):
        self._object = current_object
        self._type = regulator_type
        self._speed = speed
        self._error = error

    def work(self):
        if self.error() == 'regulator_off' or self.error() == 'container_empty':
           speed = 0.0
        else:
            speed = float(self._speed)
        self._object.change_by(self._type, speed)

    def speed(self):
        return self._speed

    def type(self):
        return self._type

    def current_object(self):
        return self._object

    def error(self):
        return self._error


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
            new_value = parameter['value'] - random_change
            min_value = float(simulation['min_value'])
            max_value = float(simulation['max_value'])
            if new_value > max_value:
                parameter['value'] = max_value
            elif new_value < min_value:
                parameter['value'] = min_value
            else:
                parameter['value'] = new_value


class Controller:
    def __init__(self, tanks, meters, regulators, other, settings):
        if not isinstance(tanks, list):
            raise ValueError
        if not isinstance(meters, list):
            raise ValueError
        if not isinstance(regulators, list):
            raise ValueError
        if not isinstance(other, list):
            raise ValueError
        self._tanks = tanks
        self._meters = meters
        self._regulators = regulators
        self._other = other
        self._settings = settings

    def check_parameter(self, parameter_id, tank):
        if not isinstance(parameter_id, str):
            raise ValueError
        if not isinstance(tank, Tank):
            raise ValueError
        for meter in self._meters:
            correct_type = meter.type() == parameter_id
            correct_object = meter.current_object() == tank
            if correct_type and correct_object:
                meter.update_value()
                reading = meter.value()
                if reading == None:
                    reading = 0
        for setting in self._settings:
            if setting['id'] == parameter_id:
                if reading < setting['alarm_low']:
                    return 'alarm_low'
                if reading > setting['alarm_high']:
                    return 'alarm_high'
                if reading < setting['low_value']:
                    return 'low'
                if reading > setting['high_value']:
                    return 'high'
                return 'normal'

    def raise_parameter(self, parameter_id, tank):
        if not isinstance(parameter_id, str):
            raise ValueError
        if not isinstance(tank, Tank):
            raise ValueError
        for regulator in self._regulators:
            correct_type = regulator.type() == parameter_id
            correct_object = regulator.current_object() == tank
            if correct_type and correct_object:
                regulator.work()

    def send_alarm(self, parameter, code, message, value):
        msg = f'{message} Current {parameter} is {value}! (Code: {code})'
        print(msg)

    def choose_failure(self, fail_chance):
        failures = [
            'regulator_on',
            'regulator_off',
            'container_empty',
            'meter_broken'
        ]
        if randrange(fail_chance) > 0:
            return None
        failure = choice(failures)
        return failure

    def set_failure(self, chance):
        failure = self.choose_failure(chance)
        if failure == None:
            return
        if failure == 'regulator_on' or failure == 'regulator_off' or failure == 'container_empty':
            objects = self._regulators
        elif failure == 'meter_broken':
            objects = self._meters
        fail_object = choice(objects)
        fail_object._error = failure

    def diagnose(self):
        failures = {}
        for meter in self._meters:
            error = meter.error()
            if error != None:
                key = f'meter_{str(id(meter))[-3:]}'
                failures[key] = error
        for regulator in self._regulators:
            error = regulator.error()
            if error != None:
                key = f'regulator_{str(id(regulator))[-3:]}'
                failures[key] = error
        return failures

    def step(self):
        msg = {
            'alarm_low': 'Parameter too low!',
            'alarm_high': 'Parameter too high!',
            'failure': 'Component failed!'
        }

        failures = self.diagnose()
        for failure in failures:
            self.send_alarm(failure, failures[failure], msg['failure'], 'broken')

        for meter in self._meters:
            id = meter.type()
            tank = meter.current_object()
            result = self.check_parameter(id, tank)
            if meter.is_raising:
                if result == "alarm_high":
                    self.send_alarm(id, result, msg[result], meter.value())
                    meter.is_raising = False
                elif result == "high":
                    meter.is_raising = False
                elif result == "alarm_low":
                    self.send_alarm(id, result, msg[result], meter.value())
                    self.raise_parameter(id, tank)
                else:
                    self.raise_parameter(id, tank)
            else:
                if result == "alarm_high":
                    self.send_alarm(id, result, msg[result], meter.value())
                elif result == "low":
                    meter.is_raising = True
                elif result == "alarm_low":
                    self.send_alarm(id, result, msg[result], meter.value())
                    meter.is_raising = True
            self.set_failure(1000)
