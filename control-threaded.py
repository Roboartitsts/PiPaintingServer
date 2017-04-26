import json
from threading import Thread
from color import Color
from paintApparatus import *
from abb import *

class Control(object):
    def __init__(self, serial_connection, apparatus):
        self.last_brush = 0
        self.last_color = Color()
        self.serial_connection = serial_connection
        self.apparatus = apparatus
        self.instructions = []
        self.delay = 0.5

    def load_instructions(self, path_to_instructions):
        print('Loading instructions located at {0}'.format(path_to_instructions))
        self.instructions = json.loads(open(path_to_instructions).read())

    def switch_brush(self, brush):
        if self.last_brush != brush:
            print('Switching to brush {0}'.format(brush))
            self.serial_connection.switch_brush(brush)

    def clean_brush(self):
        print('cleaning brush')
        self.serial_connection.moveToSafe()
        time.sleep(self.delay)
        self.serial_connection.moveApproachClean()
        time.sleep(self.delay)
        self.serial_connection.moveOverClean()
        time.sleep(self.delay)
        self.serial_connection.moveClean()
        time.sleep(self.delay)
        #self.apparatus.brush_cleaner(2)
        self.serial_connection.rinse()
        self.serial_connection.moveOverClean()
        time.sleep(self.delay)
        self.serial_connection.moveOverDry()
        time.sleep(self.delay)
        self.serial_connection.moveDry()
        time.sleep(self.delay)
        self.apparatus.brush_dryer(2)
        time.sleep(self.delay)
        self.serial_connection.moveOverDry()
        time.sleep(self.delay)
        self.serial_connection.moveOverClean()
        time.sleep(self.delay)
        self.serial_connection.rinse()
        time.sleep(self.delay)
        self.serial_connection.moveOverDry()
        time.sleep(self.delay)
        self.serial_connection.moveDry()
        time.sleep(self.delay)
        self.apparatus.brush_dryer(2)
        time.sleep(self.delay)
        self.serial_connection.moveOverDry()
        time.sleep(self.delay)
        self.serial_connection.moveToSafe()
        time.sleep(self.delay)

    def switch_or_create_color(self, ColorRGB):
        ''' Returns False if the paint color was the same, True if new paint was mixed '''
        print('creating ColorRGB R:{r}, G:{g}, B:{b}'
              .format(r=ColorRGB.red, b=ColorRGB.blue, g=ColorRGB.green))
        self.serial_connection.moveToSafe()
        if self.apparatus.create_or_activate(ColorRGB):
            self.serial_connection.mixPaint()
            return True
        self.serial_connection.getPaint(0)
        return False

    def single_step(self, step):
        print(step)
        stroke_color = Color()
        stroke_color.setRGB(step[6:9])
        stroke_color.rgb2cmyk()
#       if step[9] != self.last_brush:
#            self.switch_brush(step[9])
        to_clean = False
        if stroke_color != self.last_color:
            clean_thread = Thread(target=self.clean_brush)
            mix_thread = Thread(target=self.switch_or_create_color, args=([stroke_color]))
            #mix_thread.start()
            clean_thread.start()
            clean_thread.join()
            #mix_thread.join()
        else:
            to_clean = self.switch_or_create_color(stroke_color)
        self.serial_connection.moveToSafe()
        self.serial_connection.sendCoordQ(step[0]*2530, step[1]*2530, step[2]*2530, step[3]*2530, step[4]*2530, step[5]*2530)
        self.last_color = stroke_color

    def run(self):
        self.serial_connection.moveToSafe()
        for step in self.instructions:
            self.single_step(step)
if __name__ == '__main__':
    abb = ABBRunner(2530, 2530)
    abb.connectToSerial('/dev/ttyUSB0')
    abb.sendCanvasInfo()
    apparatus = PaintApparatus(True)
    ctrl = Control(abb, apparatus)
    ctrl.load_instructions('kmeans0999.json')
    ctrl.run()

