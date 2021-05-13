from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
# from job_boards import _main

app = Flask(__name__)

def sensor():
    print("Scheduler is alive!")

sched = BackgroundScheduler(daemon=True)
sched.add_job(sensor, 'interval', minutes=1)
sched.start()

@app.route("/")

def index():
    return "Hello."

if __name__ == "__main__":
    app.run()
