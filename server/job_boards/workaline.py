from datetime import datetime
import requests, json, sys, time
from .modules import create_temp_json
# import modules.create_temp_json as create_temp_json


data = create_temp_json.data
scraped = create_temp_json.scraped

def getJobs(date, url, company, position, location):
    date = str(date)
    title = position
    company = company
    url = url
    location = location

    # print(date, title, company, url, location)
    postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))
    
    if company not in scraped:
        data.append({
            "timestamp": postDate,
            "title": title,
            "company": company,
            "url": url,
            "location": location,
            "source": "Workaline",
            "source_url": "https://www.workaline.com",
            "category": "job"
        })
        print(f"=> workline: Added {title} for {company}")


def getResults(item):
    jobs = item["data"]

    for data in jobs:
        try:
            if "hacker" in data["source"].lower() or "stack" in data["source"]:
                date = datetime.strptime(data["published_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
                apply_url = data["url"].strip()
                company_name = data["company"].strip() if data["company"] else None
                position = data["title"].strip()
                locations_string = "Remote"
                getJobs(date, apply_url, company_name, position, locations_string)
        except:
            continue

def getURL():
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0"}

    page = 1

    while page <= 100:
        try:
            url = f"https://workaline.com/api/web/listings?page={page}&per_page=20&include=developer,engineer,frontend,backend,fullstack,front,develop,program,engine,dev,integration,data,tech,technical,cloud,microservice,query,maintenance,operation,ops,system,window,linux&exclude=sales"
            response = requests.get(url, headers=headers)

            print("=> workline: Page", page)

            data = json.loads(response.text)
            getResults(data)

            if page % 10 == 0:
                time.sleep(5)

        except:
            continue
        
        

        page += 1


def main():
    getURL()

# main()
# sys.exit(0)