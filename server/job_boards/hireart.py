import requests
import json
import sys
import random
from datetime import datetime
from bs4 import BeautifulSoup
from .modules import create_temp_json
from .modules import headers as h
# import modules.create_temp_json as create_temp_json
# import modules.headers as h


def get_jobs(url: str, company: str, position: str, location: str):
    data = create_temp_json.data
    date = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
    post_date = datetime.timestamp(
        datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))
    data.append({
        "timestamp": post_date,
        "title": position,
        # "qualifications": qualifications,
        "company": company,
        "company_logo": "https://www.hireart.com/assets/ha-headerlogo-brand-400.svg",
        "url": url,
        "location": location,
        "source": "HireArt",
        "source_url": "https://www.hireart.com",
        "category": "job"
    })
    print(f"=> hireart: Added {position} for {company}")


def get_results(item: str):
    jobs = item["jobs"]
    if jobs:
        for data in jobs:
            apply_url = data["apply_url"].strip()
            # response = requests.get(apply_url, headers=headers).text
            # soup = BeautifulSoup(response, "lxml")
            # results = soup.find("div", class_="job-requirements").find_all("li")
            # desc = [i.text for i in results]
            # desc = None

            company_name = data["company_name"].strip()
            position = data["position"].strip()
            locations_string = data["locations_string"].strip()
            get_jobs(apply_url, company_name, position, locations_string)


def get_url():
    headers = {"User-Agent": random.choice(h.headers)}
    url = "https://www.hireart.com/v1/candidates/browse_jobs?region&job_category=engineering&page=1&per=10000"
    response = requests.get(url, headers=headers)
    if response.ok:
        data = json.loads(response.text)
        get_results(data)
    else:
        print("=> hireart: Error - Response status", response.status_code)


def main():
    get_url()


# main()
# sys.exit(0)
