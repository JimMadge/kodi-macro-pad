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
    magenta=(255, 0, 255),
    violet=(128, 0, 255),
    orange=(255, 128, 0)
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
    "stop": Keycode.X,
    "toggle subtitles": Keycode.T,
    "next subtitle": Keycode.L,
    "shutdown menu": Keycode.S
}

# Define action and layer selection keys
# Keypad numbers
# | 3 | 7 | 11 | 15 |
# | 2 | 6 | 10 | 14 |
# | 1 | 5 | 9  | 13 |
# | 0 | 4 | 8  | 12 |


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


def select_layer(layer_no):
    def set_layer():
        global layer
        layer = layer_no

        set_key_colours()

    return set_layer


# Layer class
class Layer():
    def __init__(self, key_specification):
        # key_specification is an ordered list of key definitions.
        # The items of key_specification can be None for an unused key or a
        # tuple of (action, colour) where action is a keycode(int), tuple of
        # keycodes or function and colour is a tuple of three integers 0-255
        # representing the red, green and blue channels respectively.

        # Initialise actions and colours
        self.keys = []
        self.colours = []

        for key_no, item in enumerate(key_specification):
            if item is None:
                # Empty key
                self.keys.append(None)
                self.colours.append(colours["off"])
            elif isinstance(item, tuple):
                # Assign key action and colour
                action, colour = item
                self.keys.append(action)
                self.colours.append(colour)


# Define layers
layers = [
    # Layer mimicking Kodi Kore app remote plus volume
    # | context | up     | information | vol+ |
    # | left    | select | right       | vol- |
    # | back    | down   | menu        | mute |
    Layer(
        [
            (select_layer(0),             colours["green"]),
            (kodi_keymap["back"],         colours["violet"]),
            (kodi_keymap["left"],         colours["blue"]),
            (kodi_keymap["context menu"], colours["violet"]),
            (select_layer(1),             colours["orange"]),
            (kodi_keymap["down"],         colours["blue"]),
            (kodi_keymap["select"],       colours["yellow"]),
            (kodi_keymap["up"],           colours["blue"]),
            (select_layer(2),             colours["orange"]),
            (kodi_keymap["menu"],         colours["violet"]),
            (kodi_keymap["right"],        colours["blue"]),
            (kodi_keymap["information"],  colours["violet"]),
            (select_layer(3),             colours["orange"]),
            (kodi_keymap["mute"],         colours["red"]),
            (kodi_keymap["vol-"],         colours["cyan"]),
            (kodi_keymap["vol+"],         colours["green"])
        ]
    ),
    # Playback control layer
    # | toggle subtitles | next subtitle |  | vol+ |
    # | play/pause       | stop          |  | vol- |
    # | rewind           | fast forward  |  | mute |
    Layer(
        [
            (select_layer(0),                 colours["orange"]),
            (kodi_keymap["rewind"],           colours["blue"]),
            (kodi_keymap["play/pause"],       colours["green"]),
            (kodi_keymap["toggle subtitles"], colours["yellow"]),
            (select_layer(1),                 colours["green"]),
            (kodi_keymap["fast forward"],     colours["blue"]),
            (kodi_keymap["stop"],             colours["red"]),
            (kodi_keymap["next subtitle"],    colours["magenta"]),
            (select_layer(2),                 colours["orange"]),
            None,
            None,
            None,
            (select_layer(3),                 colours["orange"]),
            (kodi_keymap["mute"],             colours["red"]),
            (kodi_keymap["vol-"],             colours["cyan"]),
            (kodi_keymap["vol+"],             colours["green"])
        ]
    ),
    # System layer
    Layer(
        [
            (select_layer(0),              colours["orange"]),
            None,
            None,
            (kodi_keymap["shutdown menu"], colours["red"]),
            (select_layer(1),              colours["orange"]),
            None,
            None,
            None,
            (select_layer(2),              colours["green"]),
            None,
            (
                (Keycode.CONTROL, Keycode.ALT, Keycode.RIGHT_ARROW),
                colours["blue"]
            ),
            (
                (Keycode.CONTROL, Keycode.ALT, Keycode.LEFT_ARROW),
                colours["blue"]
            ),
            (select_layer(3),              colours["orange"]),
            None,
            (decrease_brightness,          colours["cyan"]),
            (increase_brightness,          colours["green"])
        ]
    ),
    # Empty layer
    Layer(
        [
            (select_layer(0), colours["orange"]),
            None,
            None,
            None,
            (select_layer(1), colours["orange"]),
            None,
            None,
            None,
            (select_layer(2), colours["orange"]),
            None,
            None,
            None,
            (select_layer(3), colours["green"]),
            None,
            None,
            None
        ]
    )
]

for key in keys:
    @keybow.on_press(key)
    def press_handler(key):
        action = layers[layer].keys[key.number]
        # Catch elements of Keycode
        if isinstance(action, int):
            keyboard.send(action)
        # Try to Catch a tuple of Keycodes
        elif isinstance(action, tuple):
            keyboard.send(*action)
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
