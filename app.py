import os
import RPi.GPIO as GPIO
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

GPIO.setmode(GPIO.BCM)

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

pins = {
    2 : {'name' : 'GPIO 2', 'state' : GPIO.LOW}, 
    3 : {'name' : 'GPIO 3', 'state' : GPIO.LOW},
    4 : {'name' : 'GPIO 4', 'state' : GPIO.LOW},
    5 : {'name' : 'GPIO 5', 'state' : GPIO.LOW},
    6 : {'name' : 'GPIO 6', 'state' : GPIO.LOW},
    13 : {'name' : 'GPIO 13', 'state' : GPIO.LOW},
    14 : {'name' : 'GPIO 14', 'state' : GPIO.LOW},
    16 : {'name' : 'GPIO 16', 'state' : GPIO.LOW},
    19 : {'name' : 'GPIO 19', 'state' : GPIO.LOW},
    20 : {'name' : 'GPIO 20', 'state' : GPIO.LOW},
    21 : {'name' : 'GPIO 21', 'state' : GPIO.LOW}
    }
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Set each pin as an output and make it low:
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

@app.route("/")
def main():
    return render_template('home.html')

@app.route("/pincontrol")
def pincontrol():
    # For each pin, read the pin state and store it in the pins dictionary:
    for pin in pins:
        pins[pin]['state'] = GPIO.input(pin)
    # Put the pin dictionary into the template data dictionary:
    templateData = {
        'pins' : pins
        }
    # Pass the template data into the template
    # main.html and return it to the    +++user
    return render_template('main.html', **templateData)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

@app.route('/fileupload', methods=['GET','POST'])
def upload_file():
    if request.method =='POST':
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
    return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form action="" method=post enctype=multipart/form-data>
            <p><input type=file name=file>
            <input type=submit value=Upload>
        </form>'''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)

