import serial
import time
from abb import ABBRunner
class TestABBRunner(ABBRunner):

    def __init__(self, width, height):
        self.ser = None
        self.connected = False
        self.width = width
        self.height = height

    def setSize(self, width, height):
        self.width = width
        self.height = height

    def waitRobotReady(self):
        print('fake robot ready')
        return True

    def abort(self,):
        print("Closing fake serial connection")

    def connectToSerial(self, port):
        print("fake serial connection")
        self.connected = True

    def readSerial(self,):
        print("fake serial read")
        return ''

    def readSerialLine(self,):
        print("fake read")
        return ''

    def sendSerial(self, msg):
        print(msg)
        return True
