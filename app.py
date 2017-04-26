from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
from genlist import classes
import os, sys, time
import signal
import requests
import socket
import requests
from PIL import Image
from io import BytesIO
from stepper import Stepper
from pin_control import PinControl

UPLOAD_FOLDER = 'static/img/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
pin_control = PinControl()


@app.route("/")
def main():
    url = "http://overmind.rose-hulman.edu:1700/generator"
    response = server_status()
    return render_template('home.html', status=response, genlist = classes)


@app.route("/pincontrol")
def pin_control_status():
    # Put the pin dictionary into the template data dictionary:
    templateData = {
        'pins': pin_control.pin_list
    }
    # Pass the template data into the template
    # main.html and return it to the    +++user
    return render_template('pins.html', **templateData)


@app.route("/<changepin>/<action>")
def action(change_pin, action):
    # Convert the pin from the URL into an integer:
    change_pin = int(change_pin)
    # Get the device name for the pin being changed:
    deviceName = pin_control.pin_list[change_pin]['name']
    # If the action part of the URL is "on," execute the code indented below:
    if action == "on":
        # Set the pin high:
        pin_control.set_pin(change_pin, 1)
        # Save the status message to be passed into the template:
        message = "Turned " + deviceName + " on."
    if action == "off":
        pin_control.set_pin(change_pin, 0)
        message = "Turned " + deviceName + " off."

    # Along with the pin dictionary, put the message into the template data dictionary:
    templateData = {
        'pins': pin_control.pin_list
    }

    return render_template('pins.html', **templateData)


@app.route("/steppers")
def steppers():
    return render_template('stepper.html')


# @app.route('/controlSteppers', methods=['POST'])
# def control_steppers():
#     stepper = request.form['stepper']
#     steps = request.form['stepNum']
#     delay = request.form['delayNum']
#     option = request.form['directionRadios']
#     stepper_list[stepper].run(delay, steps, option)


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
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(request.url)
    url = "http://overmind.rose-hulman.edu:1700/generator"
    response = server_status()
    return render_template('home.html', status=response, genlist=classes)

@app.route('/run_script',methods=['GET', 'POST'])
def run_script():
    return render_template('run_script.html')

@app.route('/generate', methods=['POST'])
def get_generated_image():
    imageindex = request.form['image']
    body = "{\"imageindex\":\"" + imageindex +"\"}"
    url = "http://overmind.rose-hulman.edu:1700/generator"
    response = requests.put(url, data=body)

	# Retreive generated file
    filename = "{0:0>4}.png".format(imageindex)
    url = "http://overmind.rose-hulman.edu:1700/generator" + filename
    response = requests.get(url)

    i = Image.open(BytesIO(response.content))
    i.save(filename)
    return render_template("home.html", status=response, genlist=classes)

@app.route('/decompose', methods=['POST'])
def get_decomposed_image():
    imageindex = request.form['image']
    body = "{\"imageindex\":\"" + imageindex +"\"}"
    url = "http://overmind.rose-hulman.edu:1700/decomposer"
    response = requests.get(url, data=body)

    return render_template("home.html", status=response, genlist=classes)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def server_status():
    url = "http://overmind.rose-hulman.edu:1700/generator"
    response = requests.get(url)
    return response.text

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
