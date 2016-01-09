from flask import Flask
from .433 import send_code

app = Flask(__name__)

@app.route("/one_on/")
def one_on():
    send_code(True, True, 1)
    return "1 ON!"

@app.route("/two_on/")
def two_on():
    send_code(True, True, 2)
    return "2 ON!"

@app.route("/three_on/")
def three_on():
    send_code(True, True, 3)
    return "3 ON!"

@app.route("/one_off/")
def one_on():
    send_code(True, False, 1)
    return "1 ON!"

@app.route("/two_off/")
def two_on():
    send_code(True, False, 2)
    return "2 ON!"

@app.route("/three_off/")
def three_on():
    send_code(True, False, 3)
    return "3 ON!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)