# Control Neo Trinkey (https://www.adafruit.com/product/4870)
# Neopixel LEDS over a serial interface.
# Pass LED numbers and RGB values to display.
# Copy serial_control.py to the Neo Trinkey as code.py
#
# Serial commands are of the form: leds:color
#   leds - integers 1-4 to select the LEDs to change.
#   color - hex code of color to set
#
# Multiple commands can be sent at once, separated by commas.
# color or intensity can be blank and the value won't be changed.
#
# Examples:
#   "1:FF0000" - Set LED 1 to red, with intensity at 80%.
#   "1:FF0000,2:00FF00,3:0000FF,4:000000" - Set LEDs 1, 2, and 3 to red, green, and blue. Turn LED 4 off.
#
# Inspired by Dave Parkers serial example https://github.com/daveparker/neotrinkey

import neopixel
import board
import supervisor
import time

NUM_PIXELS = 4

pixels = neopixel.NeoPixel(
        board.NEOPIXEL, NUM_PIXELS, brightness=0.2, auto_write=False, pixel_order=neopixel.GRB)

# On boot flash pixels to show ready for commands
for i in range (3):
    pixels.fill((255,255,255))
    pixels.show()
    time.sleep(0.1)
    pixels.fill((0,0,0))
    pixels.show()
    time.sleep(0.25)

colors = [(0,0,0)] * NUM_PIXELS

def serial_read():
    if supervisor.runtime.serial_bytes_available:
        return input()
    return None

def parse_commands(data):
    commands = []
    raw_commands = data.split(',')
    for raw_command in raw_commands:
        commands.append(parse_command(raw_command))
    return commands

def parse_command(command):
    try:
        leds, clr = command.split(':')
        leds = [int(x) - 1 for x in leds]
        for led in leds:
            if led >= NUM_PIXELS:
                return None

        # Convert hex string into RGB value.
        if clr == '':
            rgb = None
        else:
            rgb = tuple(int(clr[i:i+2], 16) for i in (0, 2, 4))

    except ValueError:
        return None

    return (leds, rgb)


def set_pixels(leds, rgb):
    for led in leds:

        if rgb is not None:
            colors[led] = rgb

        pixels[led] = colors[led]


def main():

    while True:
        data = serial_read()
        if data is None:
            continue

        commands = parse_commands(data)

        if not commands:
            continue

        for command in commands:
            if command is None:
                continue
            leds, clr = command
            set_pixels(leds, clr)

        pixels.show()


if __name__ == '__main__':
    main()
