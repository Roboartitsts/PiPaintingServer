
from stepper import Stepper
import RPi.GPIO as GPIO
import time
import paintApparatus

app = paintApparatus.PaintApparatus()
app.mix()
app.moveMixerOverPaint()
app.moveMixerOverClean()
#app.moveMixerDown()
app.mix()
app.moveMixerOverPaint()
# 18 paint cup position
# 26 cleaning container position

#time.sleep(4)

#GPIO.setmode(GPIO.BCM)
#for pin in [18, 26]:
#    GPIO.setup(pin, GPIO.IN)
#    print("testing pin {}".format(pin))
#    val = GPIO.input(pin)
#    print(pin, val)
#    time.sleep(1)
    #GPIO.output(pin, GPIO.LOW)

