import requests
import json
import sys
import time
import random
from datetime import datetime, timedelta
from .helpers import headers as h
from .helpers.classes import FilterJobs
# import modules.headers as h


def get_results(item: str):
    for i in item["data"]:
        date = i["published_at"].strip()
        post_date = datetime.timestamp(
            datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S"))
        apply_url = i["url"].strip()
        company_name = i["company"].strip()
        logo = "https://madewithnetworkfra.fra1.digitaloceanspaces.com/spatie-space-production/27671/vuejobs.jpg"
        position = i["title"].strip()
        description = i["description"]
        location = i["location"].strip()
        age = datetime.timestamp(datetime.now() - timedelta(days=30))
        if age <= post_date:
            FilterJobs({
                "timestamp": post_date,
                "title": position,
                "company": company_name,
                "company_logo": logo,
                #"description": description,
                "url": apply_url,
                "location": location,
                "source": "VueJobs",
                "source_url": "https://vuejobs.com/"
            })


def get_url():
    headers = {"User-Agent": random.choice(h.headers)}
    url = f"https://vuejobs.com/api/positions/search?search=&location=&jobs_per_page=1000"
    response = requests.get(url, headers=headers)
    if response.ok:
        data = json.loads(response.text)
        get_results(data)
    else:
        print("=> vuejobs: Failed. Status code:", response.status_code)


def main():
    get_url()


# main()
# sys.exit(0)
