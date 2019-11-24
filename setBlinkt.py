#!/usr/bin/python3


from sys import argv
from time import sleep
from blinkt import set_pixel, set_brightness, show, clear


def main():
    light_number = int(argv[1])
    brightness_level = float(argv[2])
    color = argv[3].split(',')
    duration = 1
    if (len(argv) == 5):
        duration = int(argv[4])
        set_pixel(light_number, int(color[0]), int(color[1]), int(color[2]), brightness=brightness_level)
        show()
        sleep(duration)

    if (len(argv) == 6):
        clear()
        set_pixel(light_number, int(color[0]), int(color[1]), int(color[2]), 0.0)
        show()

        interval = int(argv[4]) / 10
        print(f'Interval set to {interval} seconds.')

        for x in range(1, 10):
            x = round(x * 0.1, int(argv[4]))
            set_brightness(x)
            show()
            sleep(interval)


if __name__ == '__main__':
    if (len(argv) >= 5):
        main()
    else:
        print('Usage: <script> [light number: 0-7] [brightness: 0.0-1.0] "[color: 0-256,0-256,0-256]" [duration: seconds] {Gradual: True|False}')
