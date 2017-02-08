import RPi.GPIO as GPIO
import time
import sys
from enum import Enum
from stepper import Stepper
from stepper import Direction

pins = {
    2: {'name': 'GPIO 2', 'state': GPIO.LOW},
    3: {'name': 'GPIO 3', 'state': GPIO.LOW},
    4: {'name': 'GPIO 4', 'state': GPIO.LOW},
    5: {'name': 'GPIO 5', 'state': GPIO.LOW},
    6: {'name': 'GPIO 6', 'state': GPIO.LOW},
    13: {'name': 'GPIO 13', 'state': GPIO.LOW},
    14: {'name': 'GPIO 14', 'state': GPIO.LOW},
    16: {'name': 'GPIO 16', 'state': GPIO.LOW},
    19: {'name': 'GPIO 19', 'state': GPIO.LOW},
    20: {'name': 'GPIO 20', 'state': GPIO.LOW},
    21: {'name': 'GPIO 21', 'state': GPIO.LOW},
    26: {'name': 'GPIO 26', 'state': GPIO.LOW}
}
"""
0 : pallete
1 : Cyan
2 : Magenta
3 : Yellow
4 : Black
5 : White
"""
steppers = {
    0 : Stepper(0),
    1 : Stepper(1),
    2 : Stepper(2),
    3 : Stepper(3),
    4 : Stepper(4),
    5 : Stepper(5)
}

class Color(Enum):
    Cyan = 1
    Magenta = 2
    Yellow = 3
    Black = 4
    White = 5

def add(color, position, volume):
    # move pallate to color position
    dispense(color, volume)

def dispense(color, volume):
    # dispense a volume of the paint
    if color == Color.Cyan:
        steppers[1].run(50, volume, Direction.forward)
    elif color == Color.Magenta:
        steppers[2].run(50, volume, Direction.forward)
    elif color == Color.Yellow:
        steppers[3].run(50, volume, Direction.forward)
    elif color == Color.Black:
        steppers[4].run(50, volume, Direction.forward)
    elif color == Color.White:
        steppers[5].run(50, volume, Direction.forward)

def mix(seconds):
    # lower the mixer into the cup
    time.sleep(60000)
    # mix for the given number of seconds
    # raise the mixer out of the cup



class PaintApparatus:
    next_cup_steps = 8
    ten_ml_steps = 325

    def __init__(self):
        self.next_cup_steps = 8
    