from flask import Flask, render_template, Response
import RPi.GPIO as GPIO
from plugs.radioplugs import send_code
from plugs.wiredplugs import turn_on, turn_off
from flask.ext.login import LoginManager, UserMixin, login_required

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')


@app.route("/protected/", methods=["GET"])
@login_required
def protected():
    return Response(response="Hello Protected World!", status=200)


@app.route("/one_on/")
def one_on():
    send_code(True, True, 1)
    return render_template('index.html')


@app.route("/two_on/")
def two_on():
    send_code(True, True, 2)
    return render_template('index.html')


@app.route("/three_on/")
def three_on():
    send_code(True, True, 3)
    return render_template('index.html')


@app.route("/one_off/")
def one_off():
    send_code(True, False, 1)
    return render_template('index.html')


@app.route("/two_off/")
def two_off():
    send_code(True, False, 2)
    return render_template('index.html')


@app.route("/three_off/")
def three_off():
    send_code(True, False, 3)
    return render_template('index.html')


@app.route("/wire_on/")
def wire_on():
    wire = 18
    turn_on(wire)
    return render_template('index.html')


@app.route("/wire_off/")
def wire_off():
    wire = 18
    turn_off(wire)
    return render_template('index.html')


if __name__ == "__main__":
    app.config["SECRET_KEY"] = "ITSAasdasdasdxcvgSECRET"

    app.run(host='0.0.0.0', port=80, debug=True)