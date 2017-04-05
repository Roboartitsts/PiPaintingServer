
import RPi.GPIO as GPIO

class PinControl:
    pin_list = {
        2: {'name': 'GPIO 2', 'state': GPIO.LOW},
        3: {'name': 'GPIO 3', 'state': GPIO.LOW},
        4: {'name': 'GPIO 4', 'state': GPIO.LOW},
        5: {'name': 'GPIO 5', 'state': GPIO.LOW},
        6: {'name': 'GPIO 6', 'state': GPIO.LOW},
        13: {'name': 'GPIO 13', 'state': GPIO.LOW},
        14: {'name': 'GPIO 14', 'state': GPIO.LOW},
        16: {'name': 'GPIO 16', 'state': GPIO.LOW},
        19: {'name': 'GPIO 19', 'state': GPIO.LOW},
        20: {'name': 'GPIO 20', 'state': GPIO.LOW},
        21: {'name': 'GPIO 21', 'state': GPIO.LOW},
        26: {'name': 'GPIO 26', 'state': GPIO.LOW}
    }

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        for pin in self.pin_list:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

    def set_pin(self, pin, high_low):
        if high_low == 1:
            GPIO.output(pin, GPIO.HIGH)
        else:
            GPIO.output(pin, GPIO.LOW)
        # For each pin, read the pin state and store it in the pins dictionary:
        for pin in self.pin_list:
            self.pin_list[pin]['state'] = GPIO.input(pin)
