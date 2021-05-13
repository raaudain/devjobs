from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
# from flask_apscheduler import APScheduler
from job_boards import _main

# sched = APScheduler()
app = Flask(__name__)

def scanner():
    _main.main()

sched = BackgroundScheduler(daemon=True)
sched.add_job(scanner, "interval", minutes=30)
sched.start()

@app.route("/")

def index():
    return "Hello."

if __name__ == "__main__":
    # sched.add_job(id="job_scanner", func=scanner, trigger="interval", minutes=30)
    # sched.start()
    app.run(debug=True)
