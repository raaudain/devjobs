import requests
import json
import sys
import time
import random
from datetime import datetime
from .modules import headers as h
from .modules.classes import Create_JSON, Filter_Jobs
# import modules.classes as c
# import modules.headers as h


def get_results(item: str):
    scraped = Create_JSON.scraped
    date = item["created_at"]
    post_date = datetime.timestamp(
        datetime.strptime(str(date), "%Y-%m-%dT%H:%M:%S"))
    position = item["title"]
    company_name = item["employer"]["name"]
    description = item["description"]
    apply_url = item["url"]
    location = item["locations"][0]["location"]["city_state"] if len(
        item["locations"]) > 0 else "See Description"
    if company_name not in scraped:
        Filter_Jobs({
            "timestamp": post_date,
            "title": position,
            "company": company_name,
            "description": description,
            "company_logo": "https://candidate.joinbootup.com/LogoDarkText.svg",
            "url": apply_url,
            "location": location,
            "source": "Bootup",
            "source_url": "https://candidate.joinbootup.com/jobs"
        })


def get_url(ids: list):
    for i in ids:
        try:
            headers = {"User-Agent": random.choice(h.headers)}
            url = f"https://api.joinbootup.com/api/student/jobs/{i}"
            response = requests.get(url, headers=headers)
            data = json.loads(response.text)
            get_results(data["data"])
            time.sleep(0.05)
        except Exception as e:
            print(f"=> bootup: Error. {e}")


def main():
    headers = {"User-Agent": random.choice(h.headers)}
    url = "https://api.joinbootup.com/api/student/jobs?page=1&limit=200"
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)["data"]["list"]
    ids = [e["id"] for e in data]
    get_url(ids)


# main()
# sys.exit(0)
