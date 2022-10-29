import requests
import json
import sys
import time
import random
from datetime import datetime
from .helpers import create_temp_json
from .helpers import headers as h
from .helpers.classes import Filter_Jobs
# import modules.create_temp_json as create_temp_json
# import modules.headers as h


def get_results(item: str):
    jobs = item["jobs"]
    if jobs:
        for data in jobs:
            apply_url = data["applicationLink"].strip()
            date = data["added"]
            d = datetime.strptime(date, "%Y-%m-%d")
            post_date = datetime.timestamp(
                datetime.strptime(str(d), "%Y-%m-%d %H:%M:%S"))
            company_name = data["company"].strip()
            logo = data["companyLogo"].strip() if len(
                data["companyLogo"]) > 0 else "https://fullstackjob.com/img/icons/favicon-32x32.png"
            position = data["position"].strip()
            location = f"{data['location'].strip()}, " if len(
                data["location"]) > 0 else ""
            country = data["country"].strip()
            remote = " | Remote" if data["remoteOk"] != "false" else ""
            location = location+country+remote
            source = data["ownerTenant"]["host"]
            source_url = "https://"+data["ownerTenant"]["host"]
            Filter_Jobs({
                "timestamp": post_date,
                "title": position,
                "company": company_name,
                "company_logo": logo,
                "url": apply_url,
                "location": location,
                "source": source,
                "source_url": source_url
            })


def get_url():
    referers = ["https://javascriptjob.xyz/", "https://fullstackjob.com/"]
    for referer in referers:
        headers = {"User-Agent": random.choice(h.headers), "Referer": referer}
        url = "https://api.fullstackjob.com/v1/app/job"
        response = requests.get(url, headers=headers)
        if response.ok:
            data = json.loads(response.text)
            get_results(data)
        else:
            print("=> fullstackjob: Error - Response status", response.status_code)
        time.sleep(0.2)


def main():
    get_url()

# main()
# sys.exit(0)
