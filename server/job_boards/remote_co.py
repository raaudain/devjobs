from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import requests
import sys
import random
import re
from .modules import create_temp_json
from .modules.classes import Filter_Jobs
from .modules import headers as h


def getResults(item):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all(
        "a", class_="card m-0 border-left-0 border-right-0 border-top-0 border-bottom")
    for job in results:
        date = job.find("date").text
        title = job.find("span", class_="font-weight-bold larger").text
        company = "".join(
            job.find("p", class_="m-0 text-secondary").text.split("|")[0]).strip()
        url = "https://remote.co"+job["href"]
        location = "Remote"
        if "hours" in date or "hour" in date:
            hours = re.sub("[^0-9]", "", date)
            time = datetime.now() - timedelta(hours=int(hours))
            date = datetime.strftime(time, "%Y-%m-%d %H:%M")
        elif "days" in date or "day" in date:
            day = re.sub("[^0-9]", "", date)
            time = datetime.now() - timedelta(days=int(day))
            date = datetime.strftime(time, "%Y-%m-%d %H:%M")
        elif "week" in date:
            time = datetime.now() - timedelta(days=7)
            date = datetime.strftime(time, "%Y-%m-%d %H:%M")
        else:
            continue
        age = datetime.timestamp(datetime.now() - timedelta(days=30))
        post_date = datetime.timestamp(
            datetime.strptime(date, "%Y-%m-%d %H:%M"))
        if age <= post_date:
            Filter_Jobs({
                "timestamp": post_date,
                "title": title,
                "company": company,
                "url": url,
                "location": location,
                "source": "Remote.co",
                "source_url": "https://remote.co/",
                "category": "job"
            })


def getURL():
    headers = {"User-Agent": random.choice(h.headers)}
    url = "https://remote.co/remote-jobs/developer"
    response = requests.get(url, headers=headers)
    if response.ok:
        getResults(response.text)
    else:
        print("=> remote.co: Error - Response status", response.status_code)


def main():
    getURL()
