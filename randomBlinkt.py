#!/usr/bin/python3

from blinkt import set_pixel, set_brightness, show, clear
import time, colorsys, random

set_brightness(0.1)

def get_random_color():
    return (random.randint(0,255)), (random.randint(0,255)), (random.randint(0,255))

while True:
    clear()

    this_light = random.randint(0,7)

    r, g, b = get_random_color()
    set_pixel(this_light, r, g, b)
    show()
    
    try:
        for x in range(1,10):
            x = round(x * 0.1, 1)
            # print('Setting to brightness ' + str(x))
            set_brightness(x)
            show()
            time.sleep(0.001)

        for x in reversed(range(0,9)):
            brightness = round(x * 0.1, 1)
            # print('Setting to brightness ' + str(brightness))
            set_brightness(brightness)
            show()
            time.sleep(0.001)

    except Exception as e:
        print(e)


    time.sleep(0.001)
