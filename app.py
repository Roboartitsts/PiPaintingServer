import RPi.GPIO as GPIO
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
from genlist import classes
import os, sys, time
import signal
import urllib2
import socket
import requests
from PIL import Image
from io import BytesIO
from stepper import Stepper

GPIO.setmode(GPIO.BCM)

UPLOAD_FOLDER = '/static/img/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

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

stepper_list = {
    1: Stepper(0),
    2: Stepper(1),
    3: Stepper(2),
    4: Stepper(3),
    5: Stepper(4),
    6: Stepper(5),
    7: Stepper(6),
    8: Stepper(7),
    9: Stepper(-1)
}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Set each pin as an output and make it low:
for pin in pin_list:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)


@app.route("/")
def main():
    url = "http://overmind.rose-hulman.edu:1700/generator"
    response = urllib2.Request("GET", url)
    return render_template('home.html', status=response.text, genlist = classes)


@app.route("/pincontrol")
def pin_control():
    # For each pin, read the pin state and store it in the pins dictionary:
    for pin in pin_list:
        pin_list[pin]['state'] = GPIO.input(pin)
    # Put the pin dictionary into the template data dictionary:
    templateData = {
        'pins': pin_list
    }
    # Pass the template data into the template
    # main.html and return it to the    +++user
    return render_template('pins.html', **templateData)


@app.route("/<changepin>/<action>")
def action(change_pin, action):
    # Convert the pin from the URL into an integer:
    change_pin = int(change_pin)
    # Get the device name for the pin being changed:
    deviceName = pin_list[change_pin]['name']
    # If the action part of the URL is "on," execute the code indented below:
    if action == "on":
        # Set the pin high:
        GPIO.output(change_pin, GPIO.HIGH)
        # Save the status message to be passed into the template:
        message = "Turned " + deviceName + " on."
    if action == "off":
        GPIO.output(change_pin, GPIO.LOW)
        message = "Turned " + deviceName + " off."

    # For each pin, read the pin state and store it in the pins dictionary:
    for pin in pin_list:
        pin_list[pin]['state'] = GPIO.input(pin)

    # Along with the pin dictionary, put the message into the template data dictionary:
    templateData = {
        'pins': pin_list
    }

    return render_template('pins.html', **templateData)


@app.route("/steppers")
def steppers():
    return render_template('stepper.html')


@app.route('/controlSteppers', methods=['POST'])
def control_steppers():
    stepper = request.form['stepper']
    steps = request.form['stepNum']
    delay = request.form['delayNum']
    option = request.form['directionRadios']
    stepper_list[stepper].run(delay, steps, option)


@app.route('/fileupload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.sae(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(request.url)
    url = "http://overmind.rose-hulman.edu:1700/generator"
    response = urllib2.Request("GET", url)
    return render_template('home.html', status=response.text, genlist=classes)

@app.route('/generate', method=['POST'])
def get_generated_image():
    imageindex = request.form['image']
    body = "{\"imageindex\":\"" + imageindex +"\"}"
    url = "http://overmind.rose-hulman.edu:1700/generator"
    response = urllib2,Request("PUT", url, data=body)

	# Retreive generated file
    body = "{\"imageindex\":\"" + imageindex +"\"}"
    filename = "static/img/gen_image.png"
    url = "http://overmind.rose-hulman.edu:1700/generated/" + filename
    response = urllib2.Request("GET", url, data=body)

    i = Image.open(BytesIO(response.content))
    i.save(filename)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
