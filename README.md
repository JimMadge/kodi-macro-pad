# Kodi macro pad

A Keybow 2040 based macro pad for my Kodi HTPC.


## Installation

Your Keybow 2040 must be flashed with the CircuitPython firmware. Download the
[CircuitPython UF2
file](https://downloads.circuitpython.org/bin/pimoroni_keybow2040/en_GB/adafruit-circuitpython-pimoroni_keybow2040-en_GB-7.0.0.uf2).
Next hold the bootsel button of you Keybow 2040 down while connecting it to your
computer with a USB cable. A drive named `RPI-RP2` should appear. Copy the UF2
file to that directory and your Keybow will flash the firmware and reboot.

A drive called `CIRCUITPY` should now appear. You can use `install.sh` to copy
the required program and libraries to your Keybow 2040.

```bash
./install.sh /path/to/CIRCUITPY
```

See the [Circuit Python page for the Keybow
2040](https://circuitpython.org/board/pimoroni_keybow2040/) for information
about the latest version.
