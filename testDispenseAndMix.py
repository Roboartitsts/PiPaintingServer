from paintApparatus import PaintApparatus


abb = ABBRunner(2530, 2530)
abb.connectToSerial('/dev/ttyUSB0')
abb.sendCanvasInfo()
paint_app= PaintApparatus()
ctrl = Control(abb, paint_app)
#ctrl.load_instructions('test.json')
#ctrl.run()
for pin in paint_app.pin_list:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

test_color = Color()
test_color.setRGB([80, 0, 0])
test_color.rgb2cmyk()
paint_app.create_or_activate(test_color)



