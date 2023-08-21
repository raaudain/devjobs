import requests
import json
import sys
import random
from datetime import datetime
sys.path.insert(0, ".")
from src.job_boards.helpers import ProcessCompanyJobData, user_agents


process_data = ProcessCompanyJobData()

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
            process_data.filter_jobs({
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
    headers = {"User-Agent": random.choice(user_agents)}
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
