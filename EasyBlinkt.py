#!/usr/bin/python3

import logging
from sys import argv
from time import sleep
from blinkt import set_pixel, set_brightness, show, clear

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

def setBlinktLight(light_number: int, brightness_level: float, color: list, duration: int = 1, gradual: bool = False):
    logging.debug(f'''
            light_number: {light_number}
            brightness_level: {brightness_level}
            color: {color}
            duration: {duration}
            gradual: {gradual}
            ''')

    logging.info('Setting light...')

    if (gradual):
        clear()
        set_pixel(light_number, color[0], color[1], color[2], 0.0)
        show()

        # Create switch for number of steps here if duration > 10

        number_of_steps = 100
        interval = duration / number_of_steps
        logging.info(f'Interval set to {interval} seconds.')

        for x in range(1, number_of_steps):
            x = round(x * 0.01, duration)
            logging.debug(f'Setting brightness to {x}')
            set_brightness(x)
            show()
            sleep(interval)
    else:
        set_pixel(light_number, color[0], color[1], color[2], brightness=brightness_level)
        show()

        logging.info(f'Sleeping for {duration} seconds.')
        sleep(duration)


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
