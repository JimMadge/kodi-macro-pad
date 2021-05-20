from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
import board
from keybow2040 import Keybow2040
import usb_hid

# Set up Keybow
i2c = board.I2C()
keybow = Keybow2040(i2c)
keys = keybow.keys

# Set up keyboard
keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)


# Define colours
colours = dict(
    off=(0, 0, 0),
    white=(255, 255, 255),
    red=(255, 0, 0),
    green=(0, 255, 0),
    blue=(0, 0, 255),
    cyan=(0, 255, 255),
    yellow=(255, 255, 0),
    magenta=(255, 0, 255)
)


# Keypad numbers
# | 3 | 7 | 11 | 15 |
# | 2 | 6 | 10 | 14 |
# | 1 | 5 | 9  | 13 |
# | 0 | 4 | 8  | 12 |

# Kodi keyboard controls
# https://kodi.wiki/view/Keyboard_controls
kodi_keymap = {
    "context menu": Keycode.C,
    "information": Keycode.I,
    "select": Keycode.ENTER,
    "menu": Keycode.M,
    "back": Keycode.BACKSPACE,
    "right": Keycode.RIGHT_ARROW,
    "up": Keycode.UP_ARROW,
    "left": Keycode.LEFT_ARROW,
    "down": Keycode.DOWN_ARROW,
    "vol+": Keycode.EQUALS,
    "vol-": Keycode.MINUS,
    "mute": Keycode.F8,
    "play/pause": Keycode.SPACE,
    "fast forward": Keycode.F,
    "rewind": Keycode.R,
    "stop": Keycode.X
}

# layer select keys
layer_select_keys = {
    0: 0,
    4: 1,
    8: 2,
    12: 3
}

# Action keys
action_keys = [1, 2, 3,
               5, 6, 7,
               9, 10, 11,
               13, 14, 15]

# Layer mimicking Kodi Kore app remote plus volume
# | context | up     | information | vol+ |
# | left    | select | right       | vol- |
# | back    | down   | menu        | mute |
remote_layer_keys = {
    1: kodi_keymap["back"],
    2: kodi_keymap["left"],
    3: kodi_keymap["context menu"],
    5: kodi_keymap["down"],
    6: kodi_keymap["select"],
    7: kodi_keymap["up"],
    9: kodi_keymap["menu"],
    10: kodi_keymap["right"],
    11: kodi_keymap["information"],
    13: kodi_keymap["mute"],
    14: kodi_keymap["vol-"],
    15: kodi_keymap["vol+"]
}

remote_layer_colours = [
    colours["green"],
    colours["cyan"],
    colours["blue"],
    colours["cyan"],
    colours["off"],
    colours["blue"],
    colours["green"],
    colours["blue"],
    colours["off"],
    colours["cyan"],
    colours["blue"],
    colours["cyan"],
    colours["off"],
    colours["red"],
    colours["blue"],
    colours["green"]
]

# Empty layer
empty_layer_colours = [
    colours["off"],
    colours["off"],
    colours["off"],
    colours["off"],
    colours["off"],
    colours["off"],
    colours["off"],
    colours["off"],
    colours["off"],
    colours["off"],
    colours["off"],
    colours["off"],
    colours["green"],
    colours["off"],
    colours["off"],
    colours["off"],
]


# Layers
class Layer():
    def __init__(self, keys, colours):
        self.keys = keys
        self.colours = colours


layers = [
    Layer(remote_layer_keys, remote_layer_colours),
    Layer(remote_layer_keys, remote_layer_colours),
    Layer(remote_layer_keys, remote_layer_colours),
    Layer(remote_layer_keys, empty_layer_colours)
]

# Set defaults
layer = 0
brightness = 8

for key, layer in layer_select_keys.items():
    @keybow.on_press(keys[key])  # takes argument of key object
    def set_layer(key):  # This argument is actually the key object!
        # Set layer variable
        global layer
        layer = layer_select_keys[key.number]

        # Set key colours
        for key, colour in enumerate(layers[layer].colours):
            scaled_colour = (elem//brightness for elem in colour)
            keybow.set_led(key, *scaled_colour)

for key in action_keys:
    @keybow.on_press(keys[key])  # takes argument of key object
    def press_handler(key):  # This argument is actually the key object!
        keyboard.send(layers[0].keys[key.number])

while True:
    keybow.update()
