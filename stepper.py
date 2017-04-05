import time
import sys
from enum import Enum
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
pin_list = {
    2: {'name': 'GPIO 2', 'state': GPIO.LOW},
    3: {'name': 'GPIO 3', 'state': GPIO.LOW},
    4: {'name': 'GPIO 4', 'state': GPIO.LOW},
    5: {'name': 'GPIO 5', 'state': GPIO.LOW},
    6: {'name': 'GPIO 6', 'state': GPIO.LOW},
    9: {'name': 'GPIO 9', 'state': GPIO.LOW},
    10: {'name': 'GPIO 10', 'state': GPIO.LOW},
    11: {'name': 'GPIO 11', 'state': GPIO.LOW},
    12: {'name': 'GPIO 12', 'state': GPIO.LOW},
    13: {'name': 'GPIO 13', 'state': GPIO.LOW},
    14: {'name': 'GPIO 14', 'state': GPIO.LOW},
    16: {'name': 'GPIO 16', 'state': GPIO.LOW},
    19: {'name': 'GPIO 19', 'state': GPIO.LOW},
    20: {'name': 'GPIO 20', 'state': GPIO.LOW},
    21: {'name': 'GPIO 21', 'state': GPIO.LOW},
    26: {'name': 'GPIO 26', 'state': GPIO.LOW},
    17: {'name': 'GPIO 17', 'state': GPIO.LOW},
    27: {'name': 'GPIO 27', 'state': GPIO.LOW},
    22: {'name': 'GPIO 22', 'state': GPIO.LOW}

}

for pin in pin_list:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

class Direction(Enum):
    forward = 1
    backward = 2 


def setStep(stepper, w1, w2, w3, w4):
    GPIO.output(stepper.coil_A_1_pin, w1)
    GPIO.output(stepper.coil_A_2_pin, w2)
    GPIO.output(stepper.coil_B_1_pin, w3)
    GPIO.output(stepper.coil_B_2_pin, w4)


def forward(stepper, delay, steps):
    for i in range(0, steps):
        setStep(stepper, 1, 0, 1, 0)
        time.sleep(delay)
        setStep(stepper, 0, 1, 1, 0)
        time.sleep(delay)
        setStep(stepper, 0, 1, 0, 1)
        time.sleep(delay)
        setStep(stepper, 1, 0, 0, 1)
        time.sleep(delay)


def backwards(stepper, delay, steps):
    for i in range(0, steps):
        setStep(stepper, 1, 0, 0, 1)
        time.sleep(delay)
        setStep(stepper, 0, 1, 0, 1)
        time.sleep(delay)
        setStep(stepper, 0, 1, 1, 0)
        time.sleep(delay)
        setStep(stepper, 1, 0, 1, 0)
        time.sleep(delay)


def set_control(control_val):
    if control_val == 7:
        GPIO.output(16, 1)
        GPIO.output(20, 1)
        GPIO.output(21, 1)
    elif control_val == 6:
        GPIO.output(16, 1)
        GPIO.output(20, 1)
        GPIO.output(21, 0)
    elif control_val == 5:
        GPIO.output(16, 1)
        GPIO.output(20, 0)
        GPIO.output(21, 1)
    elif control_val == 4:
        GPIO.output(16, 1)
        GPIO.output(20, 0)
        GPIO.output(21, 0)
    elif control_val == 3:
        GPIO.output(16, 0)
        GPIO.output(20, 1)
        GPIO.output(21, 1)
    elif control_val == 2:
        GPIO.output(16, 0)
        GPIO.output(20, 1)
        GPIO.output(21, 0)
    elif control_val == 1:
        GPIO.output(16, 0)
        GPIO.output(20, 0)
        GPIO.output(21, 1)
    elif control_val == 0:
        GPIO.output(16, 0)
        GPIO.output(20, 0)
        GPIO.output(21, 0)
    else:
        GPIO.output(16, 0)
        GPIO.output(20, 0)
        GPIO.output(21, 0)


class Stepper:
    """control a stepper motor given control values"""
    coil_A_1_pin = 2
    coil_A_2_pin = 27
    coil_B_1_pin = 22
    coil_B_2_pin = 17

    def __init__(self, control_val):
        self.control_val = control_val

    def run(self, delay, steps, direction):
        """runs the Stepper

        Keyword arguments:
        delay -- the time between steps, min value is 50
        steps -- the number of steps to travel
        direction -- the direction for the stepper to travel
        """
        set_control(self.control_val)
        if direction == Direction.forward:
            print('going forward')
            forward(self, int(delay) / 1000.0, int(steps))
        else:
            print('going backward')
            backwards(self, int(delay) / 1000.0, int(steps))



class StepperBasic:

    def __init__(self, w1, w2, w3, w4):
        self.coil_A_1_pin = w1
        self.coil_A_2_pin = w2
        self.coil_B_1_pin = w3
        self.coil_B_2_pin = w4

    def run(self, delay, steps, direction):
        """runs the Stepper

        Keyword arguments:
        delay -- the time between steps, min value is 50
        steps -- the number of steps to travel
        direction -- the direction for the stepper to travel
        """

        if direction == Direction.forward:
            print('going forward')
            forward(self, int(delay) / 1000.0, int(steps))
        else:
            print('going backward')
            backwards(self, int(delay) / 1000.0, int(steps))

class StepperTest:
    def __init__(self, control_val):
        self.control_val = control_val

    def run(self, delay, steps, direction):
        """runs the Stepper

        Keyword arguments:
        delay -- the time between steps, min value is 50
        steps -- the number of steps to travel
        direction -- the direction for the stepper to travel
        """
        print('running stepper {0} for with {1} delay for {2} steps'.format(self.control_val, delay, steps))

