import requests
import json
import sys
import time
import random
from datetime import datetime
sys.path.insert(0, ".")
from src.job_boards.helpers import ProcessCompanyJobData, user_agents


process_data = ProcessCompanyJobData()

def get_results(item: str):
    for i in item:
        job = i["fields"]
        post_date = datetime.timestamp(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        position = job["Role"]
        company_name = job["Company Lookup"]
        logo = job["Logo"]
        apply_url = job["Website"]
        location = job["Location"]

        process_data.filter_jobs({
            "timestamp": post_date,
            "title": position,
            "company": company_name,
            "company_logo": logo,
            "url": apply_url,
            "location": location,
            "source": "Diversify Tech",
            "source_url": "https://www.diversifytech.co/"
        })


def get_url():
    try:
        headers = {"User-Agent": random.choice(user_agents)}
        url = "https://www.diversifytech.com/.netlify/functions/get-jobs-list-wp"
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)["data"]["records"]
        if len(data) > 0:
            get_results(data)
        time.sleep(0.2)
    except Exception as e:
        print(f"=> diversifytech: Status code: {response.status_code}. Error: {e}..")


def main():
    get_url()


if __name__ == "__main__":
    main()
