# Zebrafish Facility Management System

## A control system designed to monitor and regulate environmental conditions in a zebrafish facility

This project simulates a management system controlling water parameters in a zebrafish facility. It allows for adding new tanks, meters and pumps and changing their effects. By setting acceptable parameter values, and checking meters' readouts, the controller knows what regultors to turn on/off to ensure chosen conditions. In case of failure to regulate parameters properly, warning messages are sent. All parameters and components can be adjusted, before the simulation starts, and are saved for future use. When the given simulation time is over, a graph is shown, depicting change in parameters in all tanks over time. Notable features:

* Create custom setups
* Change simulation parameters
* Set custom parameter ranges
* Set warning ranges
* Set simulation time
* Create and save graphs of parameters in time
* Save settings

## How does the simulation work?

Every step the controller checks readouts of each meter and compares them to a dict of parameters it was given at the start. If the parameter in the tank read by the meter is lower than the minimum safe value or higher than the maximum safe value, it sounds and alarm. If the value is between the low and high values, nothing happens, and it checks the next parameter. If the value is higher than the high value, it turns off the regulator responsible for raising this parameter, thus letting it fall down to the chosen range naturally. If the value is lower than the low value, the corresponding regulator is turned on, raising the parameter.

## How to use the program?

1. Make sure you have downloaded all required files:
* simulation.py (runs the simulation)
* components.py (defines object classes)
* settings_reader.py (opens configuration files and creates objects)
* starting_parameters.json (saves simulation settings)
* component_settings.json (saves component settings)
* parameter_settings.json (saves controller settings)

2. Run simulation.py

3. Select your language, and follow printed instructions (commands are case-sensitive!)

Changes set in the edit mode are automatically applied for this instance of the program. To ensure value changes being remembered between sessions, use the save option for every group edited (simulation, components, controller). 

# Gui

The user interface of this program is text-based and handled mostly by set_state() and execute_state() functions in simulation.py. The program knows what to do based on the state it's in. Each frame the execute_state() function is called first, and it handles user input, ensures its validity, and returns data if needed. If it's required the returned data is used based on the state in the main program loop, and the next state is set based on the last state and given command (if any) by the next_state() function. To add a new state make sure that the used code is unique, and properly handled in set_state() and execute_state() functions. Every state except state -1 reserved for exiting the program requires a next state specified in the next_state() function, and to return a command and data in a tuple in the execute_state() function.
 
All gui options, and their respective states in the code can be seen here:
<img width="2000" height="1414" alt="ZebrafishGui (2)" src="https://github.com/user-attachments/assets/6deb30b2-ef56-444e-999d-d708f3eec4dc" />
