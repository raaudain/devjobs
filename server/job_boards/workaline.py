import requests
import json
import sys
import time
import random
from datetime import datetime
from .modules.classes import Filter_Jobs, Create_JSON
from .modules import headers as h


def get_results(item):
    scraped = Create_JSON.scraped
    jobs = item["data"]
    for data in jobs:
        date = datetime.strptime(
            data["published_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
        post_date = datetime.timestamp(
            datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S"))
        apply_url = data["url"].strip()
        company_name = data["company"].strip() if data["company"] else None
        position = data["title"].strip()
        location = "Remote"
        if company_name not in scraped:
            Filter_Jobs({
                "timestamp": post_date,
                "title": position,
                "company": company_name,
                "company_logo": "https://workaline.com/static/img/tinypng@logo-no-bg-transparent@small.png",
                "url": apply_url,
                "location": location,
                "source": "Workaline",
                "source_url": "https://www.workaline.com"
            })


def get_url():
    page = 1
    while page <= 100:
        try:
            headers = {"User-Agent": random.choice(h.headers)}
            url = f"https://workaline.com/api/web/listings?page={page}&per_page=20&include=developer,engineer,frontend,backend,fullstack,front,develop,program,engine,dev,integration,data,tech,technical,cloud,microservice,query,maintenance,operation,ops,system,window,linux&exclude=sales"
            response = requests.get(url, headers=headers)
            print("=> workline: Page", page)
            data = json.loads(response.text)
            get_results(data)
            if page % 10 == 0:
                time.sleep(5)
            else:
                time.sleep(0.05)
        except:
            continue
        page += 1


def main():
    get_url()

# main()
# sys.exit(0)
