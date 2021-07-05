from datetime import datetime, timedelta
import requests, json, sys, time
from .modules import create_temp_json
# import modules.create_temp_json as create_temp_json


data = create_temp_json.data
f = open(f"./data/params/greenhouse_io.txt", "r")
companies = [company.strip() for company in f]
f.close()

def getJobs(date, url, company, position, location):
    date = str(date)
    title = position
    company = company
    url = url
    location = location

    # age = datetime.timestamp(datetime.now() - timedelta(days=7))
    postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d %H:%M:%S%z"))
    
    data.append({
        "timestamp": postDate,
        "title": title,
        "company": company.replace("get", "").replace("join", "").capitalize(),
        "url": url,
        "location": location,
        "source": company.replace("get", "").replace("join", "").capitalize(),
        "source_url": f"https://boards.greenhouse.io/{company}",
        "category": "job"
    })
    print(f"=> greenhouse.io: Added {title} for {company}")
            


def getResults(item, name):
    data = item["departments"]
    jobs = []

    for d in data:
        if "Engineer" in d["name"] or "Tech" in d["name"] or "Data" in d["name"] or "Software" in d["name"] or "IT" in d["name"]:
            if d["jobs"]:
                jobs.extend(d["jobs"])

    for j in jobs:
        date = datetime.strptime(j["updated_at"], "%Y-%m-%dT%H:%M:%S%z")
        position = j["title"].strip()
        company_name = name
        apply_url = j["absolute_url"].strip()
        locations_string = j["location"]["name"].strip()

        getJobs(date, apply_url, company_name, position, locations_string)


def getURL():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"}

    count = 1

    for name in companies:
        try:
            url = f"https://boards-api.greenhouse.io/v1/boards/{name}/departments"

            response = requests.get(url, headers=headers).text

            data = json.loads(response)

            getResults(data, name)
            
            if count % 5 == 0:
                time.sleep(5)
                
            count+=1
        except:
            print(f"Failed to scraped: {name}")
            continue
     


def main():
    getURL()

# main()
# sys.exit(0)