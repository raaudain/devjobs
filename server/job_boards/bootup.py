import requests
import json
import sys
import time
import random
from datetime import datetime
sys.path.insert(0, ".")
from helpers import ProcessCompanyJobData, user_agents, CreateJson


process_data = ProcessCompanyJobData()

def get_results(item: str):
    scraped = CreateJson.scraped
    date = item["created_at"]
    post_date = datetime.timestamp(
        datetime.strptime(str(date), "%Y-%m-%dT%H:%M:%S"))
    position = item["title"]
    company_name = item["employer"]["name"]
    # description = item["description"]
    apply_url = item["url"]
    location = item["locations"][0]["location"]["city_state"] if len(
        item["locations"]) > 0 else "See Description"
    if company_name not in scraped:
        process_data.filter_jobs({
            "timestamp": post_date,
            "title": position,
            "company": company_name,
            #"description": description,
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
            time.sleep(0.2)
        except Exception as e:
            print(f"=> bootup: Error. {e}")


def main():
    headers = {"User-Agent": random.choice(user_agents)}
    url = "https://api.joinbootup.com/api/student/jobs?page=1&limit=200"
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)["data"]["list"]
    ids = [e["id"] for e in data]
    get_url(ids)


if __name__ == "__main__":
    main()
