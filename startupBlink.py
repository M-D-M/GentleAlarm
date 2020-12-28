#!/usr/bin/python3

from blinkt import set_pixel, set_brightness, show, clear
import time, colorsys


amplitude = 50
spacing = 360.0 / 16.0
hue = 0
blink_duration = 5


def do_one_rainbow():
    hue = int(time.time() * 100) % 360

    for x in range(8):
        offset = x * spacing
        h = ((hue + offset) % 360) / 360.0
        r, g, b = [int(c * amplitude) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)]
        set_pixel(x, r, g, b)

    show()

    time.sleep(0.001)


set_brightness(0.1)

start_time = time.time()
continue_blinking = True

while continue_blinking:
    do_one_rainbow()

    current_duration = time.time() - start_time
    if (current_duration > blink_duration):
        continue_blinking = False
