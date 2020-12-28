#!/usr/bin/python3

import logging
from sys import argv
from time import sleep
from blinkt import set_pixel, set_brightness, show, clear


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
        set_pixel(light_number, int(color[0]), int(color[1]), int(color[2]), 0.0)
        show()

        interval = duration / 10
        logging.info(f'Interval set to {interval} seconds.')

        for x in range(1, 10):
            x = round(x * 0.1, duration)
            set_brightness(x)
            show()
            sleep(interval)
    else:
        set_pixel(light_number, color[0], color[1], color[2], brightness=brightness_level)
        show()

        logging.info(f'Sleeping for {duration} seconds.')
        sleep(duration)


if __name__ == '__main__':
    if (len(argv) >= 5):
        setBlinktLight(
            light_number = int(argv[1])
            ,brightness_level = float(argv[2])
            ,color = [int(color) for color in argv[3].split(',')]
            ,duration = int(argv[4]) if len(argv) >= 5 else 1
            ,gradual = bool(argv[5]) if len(argv) == 6 else False 
        )
    else:
        logging.warning('Usage: <script> [light number: 0-7] [brightness: 0.0-1.0] "[color: 0-256,0-256,0-256]" [duration: seconds] {Gradual: True|False}')
