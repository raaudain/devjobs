from flask import Flask
from gevent.pywsgi import WSGIServer
from flask import json
from apscheduler.schedulers.background import BackgroundScheduler
from job_boards import _main


app = Flask(__name__, static_folder="data")

def scanner():
    print("=> Scanner is set to run")
    _main.main()

sched = BackgroundScheduler(daemon=True)
# sched.add_job(scanner, "interval", minutes=10)
sched.add_job(scanner, "cron", hour=4)
sched.start()

@app.route("/")
def index():
    return "Hello."

# @app.route("/api")
def data():
    with open("./data/data.json", mode="r") as f:
        text = json.load(f)
        return text


if __name__ == "__main__":
    # app.run(debug=False)
    http_server = WSGIServer(("", 5000), app)
    http_server.serve_forever()

