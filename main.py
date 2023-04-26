from flask import Flask, request, jsonify, render_template
import json
from door import GdoorControl

app = Flask(__name__)
gdc = GdoorControl()
app.debug = True
@app.route('/')
def home():
    return render_template('index.html', test = 1)

@app.route('/api/pin/state/<gpio>')
def pin_state(gpio):
    return str(gdc.switch_state(int(gpio)))

@app.route('/api/toggle')
def api():
    
    # switch one is open
    gdc.turn_off_pin(gdc.close.gpio)
    gdc.turn_off_pin(gdc.open.gpio)


    if  gdc.switch_state(gdc.switch1.gpio) ==  True:

        # open the door, leave the pin or open the door open until siwtch1 change to true
        gdc.open_door()
        return jsonify({"Message":"door was opened"})

    if gdc.switch_state(gdc.switch2.gpio) == True:

        gdc.close_door()
        return jsonify({"Message":"door was closed"})
    return jsonify({"Message":"error door state is unknown"})

if __name__ == "__main__":
    app.run(debug = True,host='0.0.0.0', port=5000)
