from datetime import datetime
import requests
import json
import sys
import time
import random
from .modules.classes import Filter_Jobs, Read_List_Of_Companies, Remove_Not_Found
from .modules import headers as h
# import modules.headers as h
# import modules.classes as c


FILE_PATH = "./data/params/workable.txt"


def get_results(item: str, param: str):
    company = item["name"]
    jobs = item["jobs"]
    for job in jobs:
        date = datetime.strptime(job["published_on"], "%Y-%m-%d")
        postDate = datetime.timestamp(
            datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S"))
        apply_url = job["url"].strip()
        company_name = company.strip()
        position = job["title"].strip()
        description = job["description"]
        remote = "Remote" if job["telecommuting"] else ""
        country = f"{job['country']}" if len(job["country"]) > 0 else ""
        city = f"{job['city']}" if len(job["city"]) > 0 else ""
        state = f"{job['state']}" if len(job["state"]) > 0 else ""
        location = f"{city} {state} {country} {remote}".strip()
        source_url = f"https://apply.workable.com/{param}/"
        Filter_Jobs({
            "timestamp": postDate,
            "title": position,
            "company": company_name,
            "company_logo": "https://www.workable.com/static/images/press/workable_logo_green.png",
            "description": description,
            "url": apply_url,
            "location": location,
            "source": company_name,
            "source_url": source_url,
        })


def get_url(companies: list):
    count = 0
    for company in companies:
        try:
            headers = {"User-Agent": random.choice(h.headers)}
            url = f"https://www.workable.com/api/accounts/{company}?details=true"
            response = requests.get(url, headers=headers)
            if response.status_code == 404:
                Remove_Not_Found(FILE_PATH, company)
            data = json.loads(response.text)
            get_results(data, company)
            if count % 9 == 0:
                time.sleep(30)
            else:
                time.sleep(0.2)
            count += 1
        except:
            if response.status_code == 429:
                print(
                    f"=> workable: Failed to scrape {company}. Status code: {response.status_code}.")
                break
            else:
                print(
                    f"=> workable: Failed for {company}. Status code: {response.status_code}.")


def main():
    companies = Read_List_Of_Companies(FILE_PATH)
    get_url(companies)


# main()
# sys.exit(0)
