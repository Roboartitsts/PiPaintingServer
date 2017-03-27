from stepper import Stepper
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
for pin in [23, 25]:
    GPIO.setup(pin, GPIO.OUT)
    print("testing pin {}".format(pin))
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(pin, GPIO.LOW)





