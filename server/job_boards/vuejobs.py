from datetime import datetime, timedelta
import requests, json, sys, time, random
from .modules import create_temp_json
from .modules import headers as h
# import modules.create_temp_json as create_temp_json
# import modules.headers as h


def getJobs(date: str, url: str, company: str, position: str, location: str):
    data = create_temp_json.data
    scraped = create_temp_json.scraped

    age = datetime.timestamp(datetime.now() - timedelta(days=30))
    postDate = datetime.timestamp(datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S"))
    
    if age <= postDate and company not in scraped:
        data.append({
            "timestamp": postDate,
            "title": position,
            "company": company,
            "url": url,
            "location": location,
            "source": "VueJobs",
            "source_url": "https://vuejobs.com/",
            "category": "job"
        })
        print(f"=> vuejobs: Added {position} for {company}")


def getResults(item: str):
    for i in item["data"]:
        date = i["published_at"].strip()
        apply_url = i["url"].strip()
        company_name = i["company"].strip()
        position = i["title"].strip()
        locations_string = i["location"].strip()
        
        getJobs(date, apply_url, company_name, position, locations_string)


def getURL():
    headers = {"User-Agent": random.choice(h.headers)}
    url = f"https://vuejobs.com/api/positions/search?search=&location=&jobs_per_page=1000"
    response = requests.get(url, headers=headers)

    if response.ok:
        data = json.loads(response.text)
        getResults(data)
    else:
        print("=> vuejobs: Failed. Status code:", response.status_code)


def main():
    getURL()

# main()
# sys.exit(0)