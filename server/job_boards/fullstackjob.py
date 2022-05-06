import requests
import json
import sys
import random
from datetime import datetime
from .modules import create_temp_json
from .modules import headers as h
# import modules.create_temp_json as create_temp_json
# import modules.headers as h


def get_jobs(url: str, date: str, company: str, position: str, location: str, logo: str, source: str, source_url: str):
    data = create_temp_json.data
    scraped = create_temp_json.scraped
    d = datetime.strptime(date, "%Y-%m-%d")
    post_date = datetime.timestamp(
        datetime.strptime(str(d), "%Y-%m-%d %H:%M:%S"))
    if company not in scraped and url not in scraped:
        data.append({
            "timestamp": post_date,
            "title": position,
            "company": company,
            "company_logo": logo,
            "url": url,
            "location": location,
            "source": source,
            "source_url": source_url,
            "category": "job"
        })
        print(f"=> fullstackjob: Added {position} for {company}")
        scraped.add(company)
        scraped.add(url)


def get_results(item: str):
    jobs = item["jobs"]
    if jobs:
        for data in jobs:
            apply_url = data["applicationLink"].strip()
            date = data["added"]
            company_name = data["company"].strip()
            logo = data["companyLogo"].strip() if len(
                data["companyLogo"]) > 0 else "https://fullstackjob.com/img/icons/favicon-32x32.png"
            position = data["position"].strip()
            location = f"{data['location'].strip()}, " if len(
                data["location"]) > 0 else ""
            country = data["country"].strip()
            remote = " | Remote" if data["remoteOk"] != "false" else ""
            locations_string = location+country+remote
            source = data["ownerTenant"]["host"]
            source_url = "https://"+data["ownerTenant"]["host"]
            get_jobs(apply_url, date, company_name, position,
                     locations_string, logo, source, source_url)


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


def main():
    get_url()

# main()
# sys.exit(0)
