from stepper import StepperBasic
import itertools
import time
import RPi.GPIO as GPIO




wires = [12,6,13,19]
for wire in wires:
    GPIO.output(wire,GPIO.HIGH)

#time.sleep(30)

permutations = itertools.permutations(wires)

for perm in permutations:
    print("Testing wires {}".format(perm))
    mixerMotor = StepperBasic(*perm)
    mixerMotor.run(15, 30, 1)
    time.sleep(5)




