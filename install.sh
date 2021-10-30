#! /usr/bin/env bash

cp code.py "$1/"

mkdir -p "$1/lib"
rm -rf "$1/lib/adafruit_hid"
rm -rf "$1/lib/adafruit_is31fl3731"

cp -rt "$1/lib/" keybow2040-circuitpython/keybow2040.py Adafruit_CircuitPython_HID/adafruit_hid/ Adafruit_CircuitPython_IS31FL3731/adafruit_is31fl3731/
