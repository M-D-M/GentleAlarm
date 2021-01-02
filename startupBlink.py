#!/usr/bin/python3

from blinkt import set_pixel, set_brightness, show, clear
import time, colorsys
import EasyBlinkt
import logging

logging.basicConfig(level = logging.DEBUG)

AMPLITUDE = 50
SPACING = 360.0 / 16.0
HUE = 0
BLINK_DURATION = 5


def do_one_rainbow():
    HUE = int(time.time() * 100) % 360

    for x in range(8):
        offset = x * SPACING
        h = ((HUE + offset) % 360) / 360.0
        r, g, b = [int(c * AMPLITUDE) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)]
        set_pixel(x, r, g, b)

    show()

    time.sleep(0.001)


set_brightness(0.1)
start_time = time.time()
continue_blinking = True

while continue_blinking:
    do_one_rainbow()
    current_duration = time.time() - start_time
    if (current_duration > BLINK_DURATION):
        continue_blinking = False

clear()

for x in range(8):
    EasyBlinkt.setBlinktLight(
        light_number = x
        ,brightness_level = 0.1
        ,color = [54, 43, 11]
        ,duration = 0.2
        ,gradual = False
    )
