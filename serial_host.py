#!/usr/bin/env python3

# Control Neo Trinkey (https://www.adafruit.com/product/4870)
# Neopixel LEDS from the command line over a serial interface.
# Set color and brightness (intensity) of each LED.
# Copy serial_control.py to the Neo Trinkey as code.py
# Inspired by Dave Parkers example https://github.com/daveparker/neotrinkey
#
# Run with '-h' for help on arguments and commands.


import argparse
import sys
import serial

DEFAULT_BAUD = 115200
DEFAULT_DEVICE = '/dev/ttyACM0' # Linux
# To find mac device run
#   ls /dev/tty.usbmodem*

COLOR_MAP = {
    'red':     'ff0000',
    'yellow':  'ffff00',
    'orange':  'ffaa00',
    'green':   '00ff00',
    'teal':    'afeeee',
    'cyan':    '00a6d6',
    'blue':    '0000ff',
    'purple':  '5a005a',
    'magenta': 'ff00ff',
    'white':   'ffffff',
    'black':   '000000',
    'off':     '000000',
    'gold':    'e7bd42',
    'pink':    'ffb6c1',
    'aqua':    '00ffff',
    'jade':    'ffd8ab',
    'amber':   'ffd8ab',
    'oldlace': 'fdf5e6',
}


class NeoTrinkey:

    def __init__(self, baud, device):
        self.baud = baud
        self.device = device

    def send(self, command):
        with serial.Serial(self.device, baudrate=self.baud) as dev:
            dev.write('{}\r'.format(command).encode())


def hcf(command, details=None):
    print('Error with command "{}" '.format(command))
    if details is None:
        details = 'Please see help for details "-h".'

    print(details)
    sys.exit(1)


def parse_commands(commands):
    formatted = []
    for command in commands:
        formatted.append(parse_command(command))

    return ','.join(formatted)


def parse_command(command):
    if command in COLOR_MAP.keys():
        command = '1234:{}'.format(command)

    parts = command.split(':')
    if len(parts) != 2:
        hcf(command)

    leds, parts = parts
    result_leds = ''

    if leds == 'all':
        leds = '1234'

    for led in leds:
        try:
            led = int(led)
        except ValueError:
            hcf(command, details='Led must be a number from 1-4.')

        if led < 1 or led > 4:
            hcf(command, details='Led must be a number from 1-4.')

        result_leds += str(led)

    parts = parts.split(',')
    if not parts:
        hcf(command, details='Specify a color, intensity or both.')

    result_color = ''
    result_intensity = '10'

    for part in parts:
        if part.isnumeric():
            part = int(part)
            if part < 1 or part > 10:
                hcf(command, details='Intensity must be between 1 and 10.')

            result_intensity = str(part)

        elif part in COLOR_MAP.keys():
            result_color = COLOR_MAP[part]
        else:
            colors = list(COLOR_MAP.keys())
            colors.sort()
            hcf(command, details=('Specify a color and/or intensity value.\n '
                                  ' Valid colors are: {}'.format(', '.join(colors))))

    return ':'.join([result_leds, result_color])


def main():
    parser = argparse.ArgumentParser(
        description='Control Neo Trinkey LEDs (NeoPixels).',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--baud', type=int, default=DEFAULT_BAUD, help='Serial baud rate')
    parser.add_argument('--device', type=str, default=DEFAULT_DEVICE, help='Serial device')
    parser.add_argument(
        'command', type=str, nargs='+',
        help=('LED control commands such as "13:red:5" (leds:color,intensity). '
              'Set LEDS 1 and 3 to red with 50%% intensity. '
              'LEDs are values 1-4 or "all". Intensity is 0-10. '
              'Type an invalid color to see a full list. '
              'Intensity or color can be left unchanged "12:blue".'
              'Specify just a color to set all LEDs. '
              'Commands are processed in the order received: '
              '"all:black,12:red" will clear all LEDs then set 1 and 2 to red at full intensity.')
    )
    args = parser.parse_args()
    neo_trinkey = NeoTrinkey(args.baud, args.device)
    neo_trinkey.send(parse_commands(args.command))


if __name__ == '__main__':
    main()