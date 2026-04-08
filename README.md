# Zebrafish Facility Management System

## A control system designed to monitor and regulate environmental conditions in a zebrafish facility

This project simulates a management system controlling water parameters in a zebrafish facility. It allows for adding new tanks, meters and pumps and changing their effects. By setting acceptable parameter values, and checking meters' readouts, the controller knows what regultors to turn on/off to ensure chosen conditions. In case of failure to regulate parameters properly, warning messages are sent. All parameters and components can be adjusted, before the simulation starts, and are saved for future use. When the given simulation time is over, a graph is shown, depicting change in parameters in all tanks over time. Notable features:

* Create custom setups
* Change simulation parameters
* Set custom parameter ranges
* Set warning ranges
* Set simulation time
* Create graphs of parameters in time
* Save settings

## How does the simulation work?

Every step the controller checks readouts of each meter and compares them to a dict of parameters it was given at the start. If the parameter in the tank read by the meter is lower than the minimum safe value or higher than the maximum safe value, it sounds and alarm. If the value is between the low and high values, nothing happens, and it checks the next parameter. If the value is higher than the high value, it turns off the regulator responsible for raising this parameter, thus letting it fall down to the chosen range naturally. If the value is lower than the low value, the corresponding regulator is turned on, raising the parameter.
