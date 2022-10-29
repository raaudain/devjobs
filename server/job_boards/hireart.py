import requests
import json
import sys
import random
sys.path.insert(0, ".")
from modules.classes import FilterJobs
from modules import headers as h
from datetime import datetime
# import modules.create_temp_json as create_temp_json
# import modules.headers as h


def get_results(item: str):
    jobs = item["jobs"]
    if jobs:
        for data in jobs:
            apply_url = data["apply_url"].strip()
            date = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
            post_date = datetime.timestamp(
                datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))
            company_name = data["company_name"].strip()
            position = data["position"].strip()
            location = data["locations_string"].strip()
            FilterJobs({
                "timestamp": post_date,
                "title": position,
                "company": company_name,
                "company_logo": "https://www.hireart.com/assets/ha-headerlogo-brand-400.svg",
                "url": apply_url,
                "location": location,
                "source": "HireArt",
                "source_url": "https://www.hireart.com",
            })


def get_url():
    headers = {"User-Agent": random.choice(h.headers)}
    url = "https://www.hireart.com/v1/candidates/browse_jobs?region&job_category=engineering&page=1&per=1000"
    response = requests.get(url, headers=headers)
    if response.ok:
        data = json.loads(response.text)
        get_results(data)
    else:
        print("=> hireart: Error - Response status", response.status_code)


def main():
    get_url()


if __name__ == "__main__":
    main()
