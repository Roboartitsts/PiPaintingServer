import RPi.GPIO as GPIO
import time
import sys
import numpy as np
from enum import Enum
from stepper import Stepper, StepperBasic
from stepper import Direction
from color import Color
import colorExtractor
import csv
import time

"""
0 : pallete
1 : Cyan
2 : Magenta
3 : Yellow
4 : Black
5 : White
"""
class CMYK(Enum):
    Cyan = 1
    Magenta = 2
    Yellow = 3
    Black = 4
    White = 5

class PaintApparatus:
    dispense_ml = 8
    steps_ml = 28
    pin_list = {
        23: {'name': 'GPIO 3', 'state': GPIO.LOW},
        24: {'name': 'GPIO 4', 'state': GPIO.LOW},
        5: {'name': 'GPIO 5', 'state': GPIO.LOW},
        6: {'name': 'GPIO 6', 'state': GPIO.LOW},
        9: {'name': 'GPIO 9', 'state': GPIO.LOW},
        10: {'name': 'GPIO 10', 'state': GPIO.LOW},
        11: {'name': 'GPIO 11', 'state': GPIO.LOW},
        13: {'name': 'GPIO 13', 'state': GPIO.LOW},
        14: {'name': 'GPIO 14', 'state': GPIO.LOW},
        19: {'name': 'GPIO 19', 'state': GPIO.LOW},
    }

    steppers = {
        0 : Stepper(0),
        1 : Stepper(1),
        2 : Stepper(2),
        3 : Stepper(3),
        4 : Stepper(4),
        5 : Stepper(5)
    }

    position_offsets = {
        1:0,
        2:126,
        3:126*2,
        4:126*3,
        5:126*4,
        'c':-8 # Todo: see if it should be 300-8 or something else
    }

    def __init__(self):
        """
        0 : pallete
        1 : Cyan
        2 : Magenta
        3 : Yellow
        4 : Black
        5 : White
        """
        self.palettePosition = 0
        self.stepsPerCup = 63
        self.maxPalettePosition = 19*self.stepsPerCup
        self.palette_colors = {}
        self.active_cup = 0

        self.activeCup = 0

        self.mixerStepper = StepperBasic(12,6,13,19)
        
        # set up position switches for the mixer arm 
         
        for pin in [18, 26]:
            GPIO.setup(pin, GPIO.IN)
            #print("testing pin {}".format(pin))
            val = GPIO.input(pin)
            #print(pin, val)
    
    def paletteGoTo(self, position):
        ''' moves the palette to the specified position in steps '''
        dist = position - self.palettePosition
        direc = Direction.forward
        if dist < 0:
            direc = Direction.backward
        self.steppers[0].run(15, dist, direc)
        self.palettePosition = position

    def getCameraColor(self):
        img = colorExtractor.captureImg()
        avg_color = colorExtractor.getMeanColor(img)
        return avg_color * 125629 / (640*480)

    def dispense(self, color, volume):
        # dispense a volume of the paint
        if color == CMYK.Cyan:
            self.steppers[1].run(50, volume, Direction.forward)
        elif color == CMYK.Magenta:
            self.steppers[2].run(50, volume, Direction.forward)
        elif color == CMYK.Yellow:
            self.steppers[3].run(50, volume, Direction.forward)
        elif color == CMYK.Black:
            self.steppers[4].run(50, volume, Direction.forward)
        elif color == CMYK.White:
            self.steppers[5].run(50, volume, Direction.forward)

    def add(self, color, position, volume):
        # move pallate to color position
        position = position * self.stepsPerCup + self.position_offsets[color]
        self.paletteGoTo(position)
        print(position)
        self.dispense(color, volume)

    def mix(self):
        self.moveMixerDown()
        # lower the mixer into the cup
        GPIO.output(11, GPIO.HIGH)
        time.sleep(15)
        GPIO.output(11, GPIO.LOW)
        # mix for the given number of seconds
        # raise the mixer out of the cup
        self.moveMixerUp()


    def moveMixerOverClean(self):
        while not self.mixer_at_clean():
            self.mixerStepper.run(15, 1, -1)

    def moveMixerOverPaint(self):
        while not self.mixer_at_paint(): 
            self.mixerStepper.run(15, 1, 1)

    def moveMixerDown(self):
        GPIO.output(10, GPIO.HIGH)
        time.sleep(13)
        GPIO.output(10, GPIO.LOW)

    def moveMixerUp(self):
        GPIO.output(9, GPIO.HIGH)
        time.sleep(13)
        GPIO.output(9, GPIO.LOW)
 
    def mixer_at_paint(self):
        ''' Switch for position is at 18'''
        return GPIO.input(18)

    def mixer_at_clean(self):
        return GPIO.input(26)
        
    def cleanMixer(self):
        self.mixerStepper.run(15, 80, 1)

    def mix_color(self, target_color):
        '''
            move to each dispenser and dispense sequentially
            move to mixer to mix
            move to camera to verify color
            target color is a ColorRGB object '''
        cmyk_colors = target_color.getCMYK()
        tot = sum(cmyk_colors)
        for index in range(len(cmyk_colors)):
            toAdd = cmyk_colors[index]*self.dispense_ml/tot
            print(toAdd)
            position = self.activeCup
            self.add(index, position, toAdd)
            time.sleep(5)
        self.palette_colors[target_color] = self.active_cup

    def changeActiveCup(self, num):
        self.activeCup = num

    def brush_cleaner(self, seconds):
        GPIO.output(24, GPIO.HIGH)
        time.sleep(seconds*1000)
        GPIO.output(24, GPIO.LOW)

    def brush_dryer(self, seconds):
        GPIO.output(23, GPIO.HIGH)
        time.sleep(seconds*1000)
        GPIO.output(23, GPIO.LOW)

    def create_or_activate(self, color):
        if color in self.palette_colors.keys():
            self.paletteGoTo(self.palette_colors[color] * self.stepsPerCup + self.position_offsets['c'])
            self.changeActiveCup(self.palette_colors[color])
            return
        self.changeActiveCup(max(self.palette_colors.values()) + 1)
        self.mix_color(color)
        self.paletteGoTo(self.active_cup * self.stepsPerCup + self.position_offsets['c'])

if __name__ == "__main__":
    print("Initiating Data collection on a color cube, generating 125 colors")
    # datafile = open('colorcube.csv')
    # csvwriter = csv.writer(datafile)

    apparatus = PaintApparatus()
    for pin in apparatus.pin_list:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
    # cyan = np.linspace(100, 0, 5)
    # magenta = np.linspace(0, 100, 5)
    # yellow = np.linspace(0, 100, 5)
    # for c in cyan:
    #     for m in magenta:
    #         for y in yellow:
    #             color = Color()
    #             color.setCMYK([c, m, y, 0, 0])
    #             color.cmyk2rgb()
    #             aparatus.mix_color(color)
    #             result = aparatus.getCameraColor()
    #             dataToWrite = [c, m, y, 0, 0]
    #             dataToWrite.extend(result)
    #             csvwriter.writerow(dataToWrite)
