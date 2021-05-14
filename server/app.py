from flask import Flask
from flask import json
from apscheduler.schedulers.background import BackgroundScheduler
# from flask_apscheduler import APScheduler
from job_boards import _main
import os

# sched = APScheduler()
app = Flask(__name__, static_folder="data")

def scanner():
    _main.main()

sched = BackgroundScheduler(daemon=True)
sched.add_job(scanner, "interval", hours=6)
sched.start()

@app.route("/")
def index():
    return "Hello."

@app.route("/data")
def data():
    filename = os.path.join(app.static_folder, "data.json")
    f = open(filename, "r")
    jsonFile = json.load(f)
    
    


if __name__ == "__main__":
    # sched.add_job(id="job_scanner", func=scanner, trigger="interval", minutes=30)
    # sched.start()
    app.run(debug=True)

