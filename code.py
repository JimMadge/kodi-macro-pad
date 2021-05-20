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

# Define action and layer selection keys
# Keypad numbers
# | 3 | 7 | 11 | 15 |
# | 2 | 6 | 10 | 14 |
# | 1 | 5 | 9  | 13 |
# | 0 | 4 | 8  | 12 |

# Layer selection keys
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

# Empty layer
empty_layer_keys = {
    1: None,
    2: None,
    3: None,
    5: None,
    6: None,
    7: None,
    9: None,
    10: None,
    11: None,
    13: None,
    14: None,
    15: None
}

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


def set_key_colours():
    for key, colour in enumerate(layers[layer].colours):
        scaled_colour = (int(elem*brightness/10) for elem in colour)
        keybow.set_led(key, *scaled_colour)


def increase_brightness():
    global brightness
    brightness += 1
    if brightness > 10:
        brightness = 10
    set_key_colours()


def decrease_brightness():
    global brightness
    brightness -= 1
    if brightness < 1:
        brightness = 1
    set_key_colours()


# Layer class
class Layer():
    def __init__(self, keys, colours):
        self.keys = keys
        self.colours = colours


# Define layers
layers = [
    # Layer mimicking Kodi Kore app remote plus volume
    # | context | up     | information | vol+ |
    # | left    | select | right       | vol- |
    # | back    | down   | menu        | mute |
    Layer(
        keys={
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
        },
        colours=[
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
    ),
    # Playback control layer
    # |        |            |              |      |
    # | rewind | play/pause | fast forward | stop |
    # |        |            |              |      |
    Layer(
        keys={
            1: None,
            2: kodi_keymap["rewind"],
            3: None,
            5: None,
            6: kodi_keymap["play/pause"],
            7: None,
            9: None,
            10: kodi_keymap["fast forward"],
            11: None,
            13: None,
            14: kodi_keymap["stop"],
            15: None
        },
        colours=[
            colours["off"],
            colours["off"],
            colours["blue"],
            colours["off"],
            colours["green"],
            colours["off"],
            colours["green"],
            colours["off"],
            colours["off"],
            colours["off"],
            colours["blue"],
            colours["off"],
            colours["off"],
            colours["off"],
            colours["red"],
            colours["off"],
        ]
    ),
    # System layer
    Layer(
        keys={
            1: None,
            2: None,
            3: None,
            5: None,
            6: None,
            7: None,
            9: None,
            10: None,
            11: None,
            13: None,
            14: decrease_brightness,
            15: increase_brightness
        },
        colours=[
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
            colours["off"],
            colours["off"],
            colours["blue"],
            colours["green"],
        ]
    ),
    Layer(empty_layer_keys, empty_layer_colours)
]
for key, layer in layer_select_keys.items():
    @keybow.on_press(keys[key])  # takes argument of key object
    def set_layer(key):  # This argument is actually the key object!
        # Set layer variable
        global layer
        layer = layer_select_keys[key.number]

        set_key_colours()

for key in action_keys:
    @keybow.on_press(keys[key])  # takes argument of key object
    def press_handler(key):  # This argument is actually the key object!
        action = layers[layer].keys[key.number]
        # Catch elements of Keycode
        if isinstance(action, int):
            keyboard.send(action)
        # Try to catch functions, not perfect as non-functions may be callable
        elif callable(action):
            action()


# Set defaults
layer = 0
# brightness [1,10]. Raw colour values are multiplied by brightness/10 and
# rounded so that 10 represents 100% brightness and 1 10%.
brightness = 5

while True:
    keybow.update()
