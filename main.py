from flask import Flask, request, jsonify, render_template
import json
from door import GdoorControl

app = Flask(__name__)

app.debug = True
@app.route('/')
def home():
    return render_template('index.html', test = 1)

@app.route('/api/toggle')
def api():
    gdc = GdoorControl()
    # switch one is open
    gdc.turn_off_pin(gdc.close.gpio)
    gdc.turn_off_pin(gdc.open.gpio)
    if not gdc.pin_state(gdc.switch1.gpio):
        # open the door, leave the pin or open the door open until siwtch1 change to true
        gdc.open_door()
    else:
        gdc.close_door()
    return jsonify({"Message":"okr"})

if __name__ == "__main__":
    app.run(debug = True,host='0.0.0.0', port=5000)
