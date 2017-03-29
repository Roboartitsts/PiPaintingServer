import * from paintApparatus
import * from abb 
import json
from color import Color

class Control(object):
    def __init__(self, serial_connection, apparatus):
        self.last_brush = 0
        self.last_color = Color()
        self.serial_connection = serial_connection
        self.apparatus = apparatus
        self.instructions = []

    def load_instructions(self, path_to_instructions):
        print('Loading instructions located at {0}'.format(path_to_instructions))
        self.instructions = json.loads(open(path_to_instructions).read())

    def switch_brush(self, brush):
        if self.last_brush != brush:
            print('Switching to brush {0}'.format(brush))
            self.serial_connection.switch_brush(brush)

    def clean_brush(self):
        print('cleaning brush')
        self.serial_connection.moveApproachClean()
        self.serial_connection.moveOverClean()
        self.serial_connection.moveClean()
        self.apparatus.brush_cleaner(2)
        self.serial_connection.moveOverClean()
        self.serial_connection.moveOverDry()
        self.serial_connection.moveDry()
        self.apparatus.brush_dryer(2)
        self.serial_connection.moveOverDry()
        self.serial_connection.moveToSafe()

    def switch_or_create_color(self, ColorRGB):
        print('creating ColorRGB R:{r}, G:{g}, B:{b}'
              .format(r=ColorRGB.red, b=ColorRGB.blue, g=ColorRGB.green))
        if self.apparatus.create_or_activate(ColorRGB):
            self.serial_connection.mixPaint()
            return
        self.serial_connection.getPaint(0)

    def single_step(self, step):
        print(step)
        stroke_color = Color()
        stroke_color.setRGB(step[6:9])
        stroke_color.rgb2cmyk()
        if step[9] != self.last_brush:
            self.switch_brush(step[9])
        if stroke_color != self.last_color:
            self.clean_brush()
            self.switch_or_create_color(stroke_color)
        self.serial_connection.sendCoordQ(step[0], step[1], step[2], step[3], step[4], step[5], step[6])

    def run(self):
        for step in self.instructions:
            self.single_step(step)
if __name__ == '__main__':
    abb = ABBRunner(2530, 2530)
    abb.connnectToSerial('/dev/ttyUSB0')
    apparatus = PaintApparatus()
    ctrl = Control(abb, apparatus)
    ctrl.load_instructions('test.json')
    ctrl.run()

