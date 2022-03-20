# Neo Trinkey Utils

Examples of code I'm using with my Neo Trinkey devices (https://www.adafruit.com/product/4870) from Adafruit

Note that the serial example is heavily inspired by Dave Parkers serial example https://github.com/daveparker/neotrinkey but I just
simplified the serial protocol a bit to take just led and rgb hex values such as ``1234:ffffff`` across the wire as bandwidth isn't
too much of a concern and allows more flexibility.

### Installing examples
1. Download the latest circuit python uf2
2. Plug in the trinkey and tap the reset button twice
3. Copy the circuit python uf2 to the disc that shows up
4. Rename the desired example to code.py and copy to the CIRCUITPYTHON disc that should now be mounted
```
cp serial_control.py /Volumes/CIRCUITPY/code.py
```
