from flask import Flask, request, jsonify, render_template
import json
from door import GdoorControl
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app = Flask(__name__)
gdc = GdoorControl()
app.debug = True
@app.route('/')
def home():
    return render_template('index.html', test = 1)

@app.route('/api/pin/state/<gpio>')
def pin_state(gpio):
    return str(gdc.switch_state(int(gpio)))

@app.route('/api/panic')
@cross_origin()
def panic_button_on():
    gdc.panic_button_on()
    return jsonify({"Message":"emergency stop activated"}) 

@app.route('/api/calibrate')
@cross_origin()
def calibration():
    gdc.reinit()
    gdc.calibrate_sequence()
    return jsonify({"Message":"calibration  activated"}) 

@app.route('/api/close')
def close():
    gdc.toggle_door(action = "close")
    return jsonify({"Message":"door was closed manualy"})

@app.route('/api/open')
def open():
    gdc.toggle_door(action = "open")
    return jsonify({"Message":"door was opened manualy"})

@app.route('/api/toggle')
@cross_origin()
def api():
    
    # switch one is open
    gdc.turn_off_pin(gdc.close.gpio)
    gdc.turn_off_pin(gdc.open.gpio)
    gdc.reinit()

    if gdc.getstate()['state'] == "lock":
        return jsonify({"Message":"error door state is lock"})

    if  gdc.switch_state(gdc.switch1.gpio) ==  True:
        # open the door, leave the pin or open the door open until siwtch1 change to true
        gdc.toggle_door(action = "open")
        return jsonify({"Message":"door was opened"})

    if gdc.switch_state(gdc.switch2.gpio) == True:

        gdc.toggle_door(action = "close")
        return jsonify({"Message":"door was closed"})

    return jsonify({"Message":"error door state is unknown"})

if __name__ == "__main__":
    app.run(debug = True,host='0.0.0.0', port=5000)
