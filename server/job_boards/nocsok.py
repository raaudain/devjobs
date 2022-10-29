from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests
import random
import sys
from .helpers import create_temp_json
from .helpers import headers as h
from .helpers.classes import FilterJobs


def get_results(item: str):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all("div", class_="w-100 jobboard-card-child")
    for job in results:
        date = datetime.strptime(job.find_all(
            "small")[1].text+" 2022", "%b %d %Y")
        title = job.find("strong").text
        company_name = job.find("small").text
        apply_url = "https://nocsok.com/" + \
            job.find("a", href=True)["href"].replace("#", "")
        location = job.find("h5").text.strip()
        age = datetime.timestamp(datetime.now() - timedelta(days=30))
        post_date = datetime.timestamp(
            datetime.strptime(str(date)[:-9], "%Y-%m-%d "))
        if age <= post_date:
            FilterJobs({
                "timestamp": post_date,
                "title": title,
                "company": company_name,
                "company_logo": "https://i.ibb.co/ygrqSj8/No-CSDegree-logo.jpg",
                "url": apply_url,
                "location": location,
                "source": "NoCSOK",
                "source_url": "https://nocsok.com/",
                "category": "job"
            })


def get_url():
    headers = {"User-Agent": random.choice(h.headers)}
    url = "https://nocsok.com/"
    response = requests.get(url, headers=headers)
    if response.ok:
        get_results(response.text)
    else:
        print("=> nocsok: Error - Response status", response.status_code)


def main():
    get_url()
