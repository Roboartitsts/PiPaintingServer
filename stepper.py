import RPi.GPIO as GPIO
import time
import sys
from enum import Enum

class Direction(Enum):
    forward = 1
    backward = 1

class Stepper:
    def __init__(self, power_a, ground_a, power_b, ground_b):
        self.coil_A_1_pin = power_a
        self.coil_A_2_pin = ground_a
        self.coil_B_1_pin = power_b
        self.coil_B_2_pin = ground_b

    def forward(delay, steps):  
        for i in range(0, steps):
            setStep(1, 0, 1, 0)
            time.sleep(delay)
            setStep(0, 1, 1, 0)
            time.sleep(delay)
            setStep(0, 1, 0, 1)
            time.sleep(delay)
            setStep(1, 0, 0, 1)
            time.sleep(delay)

    def backwards(delay, steps):  
        for i in range(0, steps):
            setStep(1, 0, 0, 1)
            time.sleep(delay)
            setStep(0, 1, 0, 1)
            time.sleep(delay)
            setStep(0, 1, 1, 0)
            time.sleep(delay)
            setStep(1, 0, 1, 0)
            time.sleep(delay)
            
    def setStep(w1, w2, w3, w4):
        GPIO.output(coil_A_1_pin, w1)
        GPIO.output(coil_A_2_pin, w2)
        GPIO.output(coil_B_1_pin, w3)
        GPIO.output(coil_B_2_pin, w4)

    def run(delay, steps, direction):
        if direction == Direction.Forward:
            forward(int(delay) / 1000.0, int(steps))
        else:
            backwards(int(delay) / 1000.0, int(steps))
        
