import serial
import time
class ABBRunner():

	def __init__(self, width, height):
		self.ser = None
		self.connected = False
		self.width = width
		self.height = height

	def sendCoord(self, x, y):
		if not self.connected:
			return False

		msg = "COORD:X:" + str(x) + ",Y:" + str(y) + ";"
		return self.sendSerial(msg)

	def sendCoordB(self, x, y):
		if not self.connected:
			return False

		msg = "COORDB:X:" + str(x) + ",Y:" + str(y) + ";"
		return self.sendSerial(msg)

	def sendCoordP(self, x, y, i):
		if not self.connected:
			return False

		msg = "COORDP:X:" + str(x) + ",Y:" + str(y) + ",I:" +str(i) +";"
		return self.sendSerial(msg)

	def sendCoordQ(self, x1, y1, x2, y2 ,x3, y3):
		if not self.connected:
			return False

		msg = "COORDQ:X:" + str(x1) + ",Y:" + str(y1) + "#" + "X:" + str(x2) + ",Y:" + str(y2) + "#" + "X:" + str(x3) + ",Y:" + str(y3) + ";"

		return self.sendSerial(msg)

	def followCurve(self):
		if not self.connected:
			return False

		msg = "GOPATH;"
		return self.sendSerial(msg)

	def griptoggle(self):
		''' By default toggles if '''
		msg = "GRIP;"
		return self.sendSerial(msg)

	def grip(self, toSqueeze):
		if toSqueeze:
			msg = "GRIPV" + str(toSqueeze)+ ";"
		return self.sendSerial(msg)

	def getPaint(self, cup = 0):
		if not self.connected:
			return False

		msg = "LATHERUP:" + str(cup) + ";"
		return self.sendSerial(msg)

	def mixPaint(self, cup = 0):
		if not self.connected:
			return False

		msg = "MIXPAINT:" + str(cup) + ";"
		return self.sendSerial(msg)

	def moveToSafe(self,):
		if not self.connected:
			return False
		return self.sendSerial("MOVETOSAFE;")


	def moveUpsideDown(self,):
		if not self.connected:
			return False
		return self.sendSerial("MOVEUPS;")

	def moveApproachClean(self,):
		if not self.connected:
			return False
		return self.sendSerial("MOVEACLEAN;")

	def moveOverClean(self,):
		if not self.connected:
			return False
		return self.sendSerial("MOVEOCLEAN;")

	def moveClean(self,):
		if not self.connected:
			return False
		return self.sendSerial("MOVECLEAN;")

	def moveOverDry(self,):
		if not self.connected:
			return False
		return self.sendSerial("MOVEODRY;")

	def moveDry(self,):
		if not self.connected:
			return False
		return self.sendSerial("MOVEDRY;")


	def next(self):
		if not self.connected:
			return False
		return self.sendSerial("NEXT;")

	def end(self,):
		if not self.connected:
			return False
		return self.sendSerial("END;")

	def decidePaint(self, col):
		if not self.connected:
			return False

		msg = "SWAP:" + col + ";"
		return self.sendSerial(msg)

	def sendCanvasInfo(self):
		if not self.connected:
			return False

		# Wait for robot to be ready
		if not self.waitRobotReady():
			return False
		# self.ser.timeout = None

		msg = "SIZE:X:" + str(self.width) + ",Y:" + str(self.height) + ";"
		return self.sendSerial(msg)

	def setSize(self, width, height):
		self.width = width
		self.height = height

	def waitRobotReady(self):
		for i in range(60):
			code = self.readSerialLine()
			print("waiting on robot...")
			if code:
				print(code)
				return True

		return False

	def abort(self,):
		self.ser.close()

	def connectToSerial(self, port):
		self.ser = serial.Serial(port, 115200, timeout=1)
		self.connected = True

	def readSerial(self,):
		msg = self.ser.read(2)
		return msg

	def readSerialLine(self,):
		msg = self.ser.readline()
		return msg

	def sendSerial(self, msg):
		if self.connected == False:
			return False

		# TODO: Try/catch?
		self.ser.write(msg.encode())
		resp = self.ser.read(1)
		# print("received command:",resp)
		while resp == '':
			time.sleep(0.1)
			resp = self.ser.read(1)
		return True