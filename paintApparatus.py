import RPi.GPIO as GPIO
import time
import sys
from enum import Enum
from stepper import Stepper

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

steppers = {
    Pallete : Stepper(0),
    Cyan : Stepper(1),
    Magenta : Stepper(2),
    Yellow : Stepper(3),
    Black : Stepper(4),
    White : Stepper(5)
}

def add(color, position, volume):
    # move pallate to color position
    dispense(color, volume)

def dispense(color, volume):
    # dispense a volume of the paint


class PaintApparatus:
    
    