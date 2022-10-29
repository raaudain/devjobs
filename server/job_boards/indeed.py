import requests
import json
import sys
import random
from datetime import datetime
from .helpers import create_temp_json
from .helpers import headers as h
from .helpers.classes import Filter_Jobs
# import modules.create_temp_json as create_temp_json
# import modules.headers as h


def get_results(item: str):
    jobs = item["jobs"]
    for j in jobs:
        date = j["data"]["create_date"]
        post_date = datetime.timestamp(
            datetime.strptime(str(date), "%Y-%m-%dT%H:%M:%S%z"))
        position = j["data"]["title"].strip()
        company_name = "Indeed"
        apply_url = "https://search.indeed.jobs/main/jobs/" + \
            j["data"]["req_id"].strip()
        location = j["data"]["full_location"].strip()
        Filter_Jobs({
            "timestamp": post_date,
            "title": position,
            "company": company_name,
            "company_logo": "https://www.indeed.jobs/wp-content/uploads/2021/02/indeed-logo-2021.svg",
            "url": apply_url,
            "location": location,
            "source": company_name,
            "source_url": "https://search.indeed.jobs/main/jobs"
        })


def get_url():
    page = 1
    while True:
        try:
            headers = {"User-Agent": random.choice(h.headers)}
            url = f"https://search.indeed.jobs/api/jobs?categories=Marketing|Search%20Quality|Security|Software%20Engineering&page={page}&limit=100&sortBy=posted_date&descending=true"
            response = requests.get(url, headers=headers)
            data = json.loads(response.text)

            if len(data["jobs"]) > 0:
                get_results(data)
                page += 1
            else:
                break
        except:
            print(
                f"=> indeed: Error for page {page}. Status code: {response.status_code}.")
            break


def main():
    get_url()


# main()
# sys.exit(0)
