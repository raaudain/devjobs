from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests, sys, random
from .modules import create_temp_json
from .modules import headers as h
# import modules.create_temp_json as create_temp_json
# import modules.headers as h


def get_jobs(item: str):
    data = create_temp_json.data

    date = datetime.strftime(datetime.now(), "%Y-%m-%d")
    title = item.text
    company = "ClickUp"
    url = "https://clickup.com"+item["href"]
    location = "See description"

    post_date = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d"))

    data.append({
        "timestamp": post_date,
        "title": title,
        "company": company,
        "url": url,
        "location": location,
        "source": "ClickUp",
        "source_url": "https://clickup.com",
        "category": "job"
    })
    print(f"=> clickup: Added {title}")

def get_results(item: str):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all("a", {"class": "current-vacancies__jobs_description"})

    for i in results:
        if "Engineer" in i.text or "Tech" in i.text or "Support" in i.text or "IT " in i.text:
            get_jobs(i)

def get_url():
    headers = {"User-Agent": random.choice(h.headers)}
    url = f"https://clickup.com/careers"
    response = requests.get(url, headers=headers)

    if response.ok: get_results(response.text)
    else: print("=> clickup: Error - Response status", response.status_code)

def main():
    get_url()

# main()
# sys.exit(0)