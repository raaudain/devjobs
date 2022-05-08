from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests
import sys
import random
from .modules import headers as h
from .modules.classes import Filter_Jobs
# import modules.create_temp_json as create_temp_json
# import modules.headers as h


def get_results(item: str):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all("tr")
    for job in results:
        if job.find("time"):
            date = job.find("time")["datetime"].replace("T", " ")[:-9]
            post_date = datetime.timestamp(
                datetime.strptime(str(date), "%Y-%m-%d %H:%M%S"))
            position = job.find("h2", {"itemprop": "title"}).text.strip()
            company_name = job.find("h3", {"itemprop": "name"}).text.strip()
            logo = job.find("img", class_="logo lazy lazyloaded")["src"].replace(
                ",quality=50", "") if job.find("img", class_="logo lazy lazyloaded", src=True) else None
            apply_url = "https://remoteok.io" + \
                job.find("a", class_="preventLink", href=True)["href"]
            location = job.find("div", class_="location tooltip").text.strip(
            ) if job.find("div", class_="location tooltip") else "Remote"
            age = datetime.timestamp(datetime.now() - timedelta(days=30))
            if age <= post_date:
                Filter_Jobs({
                    "timestamp": post_date,
                    "title": position,
                    "company": company_name,
                    "company_logo": logo,
                    "url": apply_url,
                    "location": location,
                    "source": "Remote OK",
                    "source_url": "https://remoteok.io/"
                })


def get_url():
    headers = {"User-Agent": random.choice(h.headers)}
    url = "https://remoteok.io/remote-dev-jobs"
    response = requests.get(url, headers=headers)
    if response.ok:
        get_results(response.text)
    else:
        print("=> remoteok: Error - Response status", response.status_code)


def main():
    get_url()


# main()
# sys.exit(0)
