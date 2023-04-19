from flask import Flask, request, jsonify, render_template
import json
from door import GdoorControl

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html', test = 1)

@app.route('/api/toggle')
def api():
    gdc = GdoorControl()
    gdc.toggle_pin(17)
    gdc.toggle_pin(22)
    return jsonify({"Message":"This is your flask app with docker"})

if __name__ == "__main__":
    app.run(debug = True, host='0.0.0.0', port=5000)