from flask import Flask
from flask_apscheduler import APScheduler

app = Flask(__name__, static_folder="/data")

@app.route("/")

def index():
    return "Hello, Ramon"

if __name__ == "__main__":
    app.run()
