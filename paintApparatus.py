import RPi.GPIO as GPIO
import time
from enum import Enum
from stepper import Stepper, StepperBasic
from stepper import Direction
from color import Color
import colorExtractor

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
        print("dispensing {0} of {1} color".format(volume, color))
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
            print('Mixing paint: {}'.format(target_color.getCMYK()))
            position = self.activeCup
            self.add(index + 1, position, toAdd)
            time.sleep(5)
        self.palette_colors[target_color] = self.active_cup
        self.paletteGoTo(self.active_cup * self.stepsPerCup + self.position_offsets['c'])

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
            return False
        self.changeActiveCup(max(self.palette_colors.values() + [-1]) + 1)
        self.mix_color(color)
        self.paletteGoTo(self.active_cup * self.stepsPerCup + self.position_offsets['c'])
        return True

if __name__ == "__main__":
    print("Initiating Data collection on a color cube, generating 125 colors")
    # datafile = open('colorcube.csv')
    # csvwriter = csv.writer(datafile)

    paint_app = PaintApparatus()
    for pin in paint_app.pin_list:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

    test_color = Color()
    test_color.setRGB([80, 0, 0])
    test_color.rgb2cmyk()
    paint_app.create_or_activate(test_color)
