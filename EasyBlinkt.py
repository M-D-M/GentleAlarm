#!/usr/bin/python3

import logging
import os
import tempfile
from sys import argv
from time import sleep
from blinkt import set_pixel, set_brightness, show, clear

DEBUG = True
STATE_FILE = os.path.join(tempfile.gettempdir(), 'GentleAlarm_State.json')
STEP_DICT = {
    "long": {
        "steps": 100
        ,"multiplier": 0.01
    }
    ,"short": {
        "steps": 10
        ,"multiplier": 0.1
    }
}


def getLightsInUse():
    lights_in_use_list = []

    if os.path.exists(STATE_FILE):
        with open(file = STATE_FILE, mode = 'r') as state_file:
            state_file_data = state_file.read()
            logging.debug(f'State file data: "{state_file_data}"')

            if (state_file_data is not ""):
                lights_in_use_list = [int(light) for light in state_file_data.split('|')]

    return lights_in_use_list


def setLightsInUse(lights_in_use_list: list):
    try:
        with open(file = STATE_FILE, mode = 'w') as state_file:
            state_file.write('|'.join([str(light) for light in lights_in_use_list]))
    except:
        raise


def tryToToggleLightInUse(light_number: int, send_power_to_light: bool):
    lights_in_use = getLightsInUse()
    
    # If we want to turn on the light, but the light is already in use
    if (send_power_to_light and light_number in lights_in_use):
        raise ValueError("Cannot turn on light becuase light is already in use!")

    # If we want to turn off the light
    elif (not send_power_to_light and light_number in lights_in_use):
        logging.debug(f'Marking light {light_number} as no longer in use.')
        lights_in_use.remove(light_number)

    # If we want to turn on the light, and the light is not in use
    else:
        logging.debug(f'Marking light {light_number} as in use.')
        lights_in_use.append(light_number)

    setLightsInUse(lights_in_use)


def setBlinktLight(light_number: int, brightness_level: float, color: list, duration: int = 1, gradual: bool = False):
    logging.debug(f'''
            light_number: {light_number}
            brightness_level: {brightness_level}
            color: {color}
            duration: {duration}
            gradual: {gradual}
            ''')

    logging.info('Setting light...')

    try:
        tryToToggleLightInUse(light_number = light_number, send_power_to_light = True)

        try:
            if (gradual):
                # Switch for number of steps here if duration > 10
                interval_config = 'short'
                if (duration > 10):
                    interval_config = 'long'

                steps = STEP_DICT[interval_config]['steps']
                multiplier = STEP_DICT[interval_config]['multiplier']

                logging.debug(f'Number of steps: {steps} -- multiplier: {multiplier}')

                # Set variables for gradual light change
                number_of_steps = int(steps * brightness_level)
                interval = duration / number_of_steps
                logging.info(f'Interval set to {interval} seconds.')

                # Begin slowly increasing light intensity
                for x in range(1, number_of_steps):
                    x = round(x * multiplier, duration)
                    logging.debug(f'Setting brightness to {x}')
                    set_pixel(light_number, color[0], color[1], color[2], x)
                    show()
                    logging.info(f'Sleeping for {interval} seconds')
                    sleep(interval)
            else:
                # Immediately set light intensity
                set_pixel(light_number, color[0], color[1], color[2], brightness=brightness_level)
                show()

                logging.info(f'Sleeping for {duration} seconds.')
                sleep(duration)
        except:
            logging.exception(f'Exception while trying to interact with blinkt subsystem!')

        logging.info('Clearing light...')
        set_pixel(light_number, 0, 0, 0, 0)

        tryToToggleLightInUse(light_number = light_number, send_power_to_light = False)
    except:
        logging.exception('Exception while trying to set or clear light!')
        raise
        


if __name__ == '__main__':
    logging.basicConfig(level = logging.DEBUG if DEBUG else logging.INFO)

    if (len(argv) >= 5):
        setBlinktLight(
            light_number = int(argv[1])
            ,brightness_level = float(argv[2])
            ,color = [int(color) for color in argv[3].split(',')]
            ,duration = int(argv[4]) if len(argv) >= 5 else 1
            ,gradual = True if (len(argv) == 6 and argv[5] == "True") else False 
        )
    else:
        logging.warning('Usage: <script> [light number: 0-7] [brightness: 0.0-1.0] "[color: 0-256,0-256,0-256]" [duration: seconds] {Gradual: True|False}')
