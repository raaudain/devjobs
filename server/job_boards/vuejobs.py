from datetime import datetime, timedelta
import requests, json, sys, time, random
from .modules import create_temp_json
from .modules import headers as h
# import modules.create_temp_json as create_temp_json
# import modules.headers as h


data = create_temp_json.data

def getJobs(date, url, company, position, location):
    date = str(date)
    title = position
    company = company
    url = url
    location = location

    # print(date, title, company, url, location)
    age = datetime.timestamp(datetime.now() - timedelta(days=14))
    postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))
    
    if age <= postDate:
        data.append({
            "timestamp": postDate,
            "title": title,
            "company": company,
            "url": url,
            "location": location,
            "source": "VueJobs",
            "source_url": "https://vuejobs.com/",
            "category": "job"
        })
        print(f"=> vuejobs: Added {title} for {company}")


def getResults(item):
    for i in item["data"]:
        date = i["published_at"].strip()
        apply_url = i["url"].strip()
        company_name = i["company"].strip()
        position = i["title"].strip()
        locations_string = i["location"].strip()
        
        getJobs(date, apply_url, company_name, position, locations_string)


def getURL():
    headers = {"User-Agent": random.choice(h.headers)}

    try:
        url = f"https://vuejobs.com/api/positions/search?search=&location=&jobs_per_page=1000"
        response = requests.get(url, headers=headers)

        data = json.loads(response.text)
        getResults(data)

    except:
        print("=> vuejobs: Failed")
        pass



def main():
    getURL()

# main()
# sys.exit(0)