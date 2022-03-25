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

## Adding ser2net
ser2net allows sharing of serial ports over a network connection and can be used to bridge the USB port serial connection
to TCP for access from inside a docker container or other application with local network access.

To install:
```
sudo apt install -y ser2net
```

As of March 25 2022, the default install of ser2net on Raspbian Bullseye will not work as the network needs to be available
before starting the service.  To fix this `sudo nano /lib/systemd/system/ser2net.service` then edit the `[Unit]` section
as below. You may also wish to get the server to `Restart=always`

```
[Unit]
Description=Serial port to network proxy
Documentation=man:ser2net(8)
After=network-online.target
Wants=network-online.target

[Service]
EnvironmentFile=-/etc/default/ser2net
ExecStart=/usr/sbin/ser2net -n -c $CONFFILE -P /run/ser2net.pid
Type=exec
Restart=always

[Install]
WantedBy=multi-user.target
```

Alternatively replace the example one with the example in this repo.
```
sudo wget -O /lib/systemd/system/ser2net.service https://raw.githubusercontent.com/martinwoodward/trinkey/HEAD/ser2net.service
```


Next you will want to edit the `/etc/ser2net.yaml' file as per the [example](ser2net.yaml)

```
sudo wget -O /etc/ser2net.yaml https://raw.githubusercontent.com/martinwoodward/trinkey/HEAD/ser2net.yaml
```

Finally you can restart the service
```
sudo systemctl restart ser2net
```

Then test it by telnet-ing to port 2000 on the machine.

Assuming that works, reboot the pi and then check the port has come up once restarted.
