import RPi.GPIO as GPIO
import time
import sys
import numpy as np
from enum import Enum
from stepper import Stepper
from stepper import Direction
import colorExtractor
import csv
import time

pins = {
    2: {'name': 'GPIO 2', 'state': GPIO.LOW},
    3: {'name': 'GPIO 3', 'state': GPIO.LOW},
    4: {'name': 'GPIO 4', 'state': GPIO.LOW},
    5: {'name': 'GPIO 5', 'state': GPIO.LOW},
    6: {'name': 'GPIO 6', 'state': GPIO.LOW},
    9: {'name': 'GPIO 9', 'state': GPIO.LOW},
    10: {'name': 'GPIO 10', 'state': GPIO.LOW},
    11: {'name': 'GPIO 11', 'state': GPIO.LOW},
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




class PaintApparatus:
        
    def __init__(self):
        """
        0 : pallete
        1 : Cyan
        2 : Magenta
        3 : Yellow
        4 : Black
        5 : White
        """
        self.steppers = {
        0 : Stepper(0),
        1 : Stepper(1), 
        2 : Stepper(2),
        3 : Stepper(3),
        4 : Stepper(4),
        5 : Stepper(5)
        }

        self.positionOffsets = {
        1:0,
        2:126,
        3:126*2,
        4:126*3,
        5:126*4,
        'c':-8 # Todo: see if it should be 300-8 or something else
        }

        self.palettePosition = 0
        self.stepsPerCup = 63
        self.maxPalettePosition = 19*self.stepsPerCup

        self.activeCup = 0


    
    def paletteGoTo(self, position):
        ''' moves the palette to the specified position in steps '''
        dist = position - self.palettePosition
        dir = Direction.forward
        if dist < 0:
            dir = Direction.backward
            
        self.steppers[0].run(15, dist, dir)
        self.palettePosition = position

    def getCameraColor(self):
        img = colorExtractor.captureImg()
        avgColor = colorExtractor.getMeanColor(img)
        return avgColor * 125629 / (640*480)

    def dispense(self, color, volume):
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

    def add(self, color, position, volume):
        # move pallate to color position
        self.paletteGoTo(position)
        print(position)
        self.dispense(color, volume)

    def mix(seconds):
        GPIO.output(10, GPIO.HIGH)
        time.sleep(13000)
        GPIO.output(10, GPIO.LOW)
        # lower the mixer into the cup
        GPIO.output(11, GPIO.HIGH)
        time.sleep(15000)
        GPIO.output(11, GPIO.LOW)
        # mix for the given number of seconds
        # raise the mixer out of the cup
        GPIO.output(9, GPIO.HIGH)
        time.sleep(13000)
        GPIO.output(9, GPIO.LOW)
    
        

    def mixColor(self,targetColor):
        ''' 
         move to each dispenser and dispense sequentially
         move to mixer to mix
         move to camera to verify color
         target color is in the form [C M Y B W] '''
        
        for index in range(len(targetColor)):
	    print(targetColor[index])
            self.add(index, self.activeCup*self.stepsPerCup + self.positionOffsets[index+1], targetColor[index])
            time.sleep(5)


    def changeActiveCup(self, num):
        self.activeCup = num



if __name__ == "__main__":
    for pin in pin_list:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
    print "Initiating Data collection on a color cube, generating 125 colors"
    datafile = open('colorcube.csv')
    csvwriter = csv.writer(datafile)
    
    aparatus = PaintApparatus()
    cyan = np.linspace(100, 0, 5)
    magenta = np.linspace(0, 100, 5)
    yellow = np.linspace(0, 100, 5)
    for c in cyan:
        for m in magenta:
            for y in yellow:
                mixColor([c,m,y,0,0])
                result = aparratus.getCameraColor()
                dataToWrite = [c,m,y,0,0]
                dataToWrite.extend(result)
                csvwriter.writerow(dataToWrite)
