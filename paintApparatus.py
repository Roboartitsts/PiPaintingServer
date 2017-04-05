import RPi.GPIO as GPIO
import time
from enum import Enum
from stepper import Stepper, StepperBasic, StepperTest
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
        2:126.66,
        3:126.66*2,
        4:126.66*3,
        5:126.66*4,
        'c':63.33*14 # Todo: see if it should be 300-8 or something else
    }

    def __init__(self, debug=False):
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
        self.debug = debug
        self.activeCup = 0

        # self.mixerStepper = StepperBasic(12,6,13,19)

        if debug:
            self.steppers = []
            self.steppers.append(Stepper(0))
            for i in range(1, 5):
                self.steppers.append(StepperTest(i))

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
            dist = abs(dist)
        self.steppers[0].run(5, dist, direc)
        self.palettePosition = position

    def getCameraColor(self):
        img = colorExtractor.captureImg()
        avg_color = colorExtractor.getMeanColor(img)
        return avg_color * 125629 / (640*480)

    def dispense_old(self, color, volume):
        # dispense a volume of the paint
        volume = volume * self.steps_ml
        print("dispensing {0} of color {1}".format(volume, color))
        if color == CMYK.Cyan:
            self.steppers[1].run(15, volume, Direction.forward)
        elif color == CMYK.Magenta:
            self.steppers[2].run(15, volume, Direction.forward)
        elif color == CMYK.Yellow:
            self.steppers[3].run(15, volume, Direction.forward)
        elif color == CMYK.Black:
            self.steppers[4].run(15, volume, Direction.forward)
        elif color == CMYK.White:
            self.steppers[5].run(15, volume, Direction.forward)

    def dispense(self, color, volume):
        # dispense a volume of the paint
        volume = volume * self.steps_ml
        print("dispensing {0} of color {1}".format(volume, color))
        speed = 5
        backsteps = 0
        if volume > 40:
            backsteps = 40

        if color == CMYK.Cyan:
            self.steppers[1].run(speed, volume + 40, Direction.forward)
            time.sleep(0.25)
            self.steppers[1].run(speed, 40, Direction.backward)
            time.sleep(1.5)
            self.steppers[1].run(speed, 10, Direction.forward)
            self.steppers[1].run(speed, 10, Direction.backward)
        elif color == CMYK.Magenta:
            self.steppers[2].run(speed, volume + 40, Direction.forward)
            time.sleep(0.25)
            self.steppers[2].run(speed, 40, Direction.backward)
            time.sleep(1.5)
            self.steppers[2].run(speed, 10, Direction.forward)
            self.steppers[2].run(speed, 10, Direction.backward)
        elif color == CMYK.Yellow:
            volume = volume/2.0
            self.steppers[3].run(25, volume + 40, Direction.forward)
            time.sleep(0.25)
            self.steppers[3].run(25, 40, Direction.backward)
        elif color == CMYK.Black:
            return
            self.steppers[4].run(speed, volume + 10, Direction.forward)
            time.sleep(0.25)
            self.steppers[4].run(speed, 40, Direction.backward)
        elif color == CMYK.White:
            return
            self.steppers[5].run(15, volume + 10, Direction.forward)
            time.sleep(0.25)
            self.steppers[5].run(15, 40, Direction.backward)

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
        print('Mixing paint: {}'.format(target_color.getCMYK()))
        for index in range(0,3):
            toAdd = cmyk_colors[index]*self.dispense_ml/tot
            position = self.activeCup
            self.add(index + 1, position, toAdd)
            if not self.debug:
                time.sleep(15)
            else:
                time.sleep(1)
        self.palette_colors[target_color] = self.activeCup
        self.paletteGoTo(self.activeCup * self.stepsPerCup + self.position_offsets['c'])

    def changeActiveCup(self, num):
        self.activeCup = num

    def brush_cleaner(self, seconds):
        GPIO.output(24, GPIO.HIGH)
        time.sleep(seconds)
        GPIO.output(24, GPIO.LOW)

    def brush_dryer(self, seconds):
        GPIO.output(23, GPIO.HIGH)
        time.sleep(seconds)
        GPIO.output(23, GPIO.LOW)

    def create_or_activate(self, color):
        if color in self.palette_colors.keys():
            self.paletteGoTo(self.palette_colors[color] * self.stepsPerCup + self.position_offsets['c'])
            self.changeActiveCup(self.palette_colors[color])
            return False
        self.changeActiveCup(max(self.palette_colors.values() + [-1]) + 1)
        self.mix_color(color)
        self.paletteGoTo(self.activeCup * self.stepsPerCup + self.position_offsets['c'])
        return True

if __name__ == "__main__":
    print("Initiating Data collection on a color cube, generating 125 colors")
    # datafile = open('colorcube.csv')
    # csvwriter = csv.writer(datafile)

    paint_app = PaintApparatus(True)
    for pin in paint_app.pin_list:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

    test_color = Color()
    test_color.setRGB([80, 0, 0])
    test_color.rgb2cmyk()
    paint_app.create_or_activate(test_color)

    print('active cup {0}, palettePosition {1}'.format(paint_app.activeCup,
paint_app.palettePosition))
    time.sleep(10)

    test_color1 = Color()
    test_color1.setRGB([255, 255, 255])
    test_color1.rgb2cmyk()
    paint_app.create_or_activate(test_color1)
    time.sleep(1)
    paint_app.create_or_activate(test_color)

    #test_color2 = Color()
    #test_color2.setRGB([36, 69, 150])
    #test_color2.rgb2cmyk()
    #paint_app.create_or_activate(test_color2)
