#!/usr/bin/python3

import logging
import os
from sys import argv
from time import sleep
from blinkt import set_pixel, set_brightness, show, clear

LIGHT_IN_USE_VAR="BLINKT_LIGHTS_IN_USE"
STEP_DICT = {
    "short": {
        "steps": 100
        ,"multiplier": 0.01
    }
    ,"long": {
        "steps": 10
        ,"multiplier": 0.1
    }
}

'''
def (light_number: int):
    if (not os.environ.get(LIGHT_IN_USE_VAR))
    lights_in_use = [int(light) for light in os.environ['BLINKT_LIGHTS_IN_USE'].split('|')]
    
    if light_number in lights_in_use:
'''

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
        if (gradual):
            # Create switch for number of steps here if duration > 10

            number_of_steps = int(100 * brightness_level)
            interval = duration / number_of_steps
            logging.info(f'Interval set to {interval} seconds.')

            for x in range(1, number_of_steps):
                x = round(x * 0.01, duration)
                logging.debug(f'Setting brightness to {x}')
                set_pixel(light_number, color[0], color[1], color[2], x)
                show()
                logging.info(f'Sleeping for {interval} seconds')
                sleep(interval)
        else:
            set_pixel(light_number, color[0], color[1], color[2], brightness=brightness_level)
            show()

            logging.info(f'Sleeping for {duration} seconds.')
            sleep(duration)
    except:
        logging.exception(f'Exception while trying to set light!')

    logging.info('Clearing light...')
    set_pixel(light_number, 0, 0, 0, 0)


if __name__ == '__main__':
    logging.basicConfig(level = logging.DEBUG)

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
