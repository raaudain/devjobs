from datetime import datetime
import requests, json, sys
from .modules import create_temp_json
# import modules.create_temp_json as create_temp_json


data = create_temp_json.data

def getJobs(date, url, company, position, location):
    date = str(date)
    title = position
    company = company
    url = url
    location = location

    # print(date, title, company, url, location)
    postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))
    
    data.append({
        "timestamp": postDate,
        "title": title,
        "company": company,
        "url": url,
        "location": location,
        "source": company,
        "source_url": "https://careers.twitter.com/",
        "category": "job"
    })
    print(f"=> twitter: Added {title} for {company}")


def getResults(item):
    jobs = item["results"]

    for data in jobs:
        date = datetime.fromtimestamp(data["modified"] / 1e3)
        apply_url = data["url"].strip()
        company_name = "Twitter"
        position = data["title"].strip()
        locations = ""
        for i in data["locations"]: locations += i["title"]+", "
        locations_string = locations.rstrip(", ")
        getJobs(date, apply_url, company_name, position, locations_string)

def getURL():
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0"}

    url = "https://careers.twitter.com/content/careers-twitter/en/roles.careers.search.json?location=&team=careers-twitter:sr/team/software-engineering,careers-twitter:sr/team/it-it-enterprise-applications,careers-twitter:sr/team/data-science-and-analytics,careers-twitter:sr/team/customer-support-and-operations&offset=0&limit=1000&sortBy=modified&asc=false"
    response = requests.get(url, headers=headers)

    if response.ok:
        data = json.loads(response.text)
        getResults(data)
    else:
        print("=> twitter: Error - Response status", response.status_code)
    
    # print(data)
     


def main():
    getURL()

# main()
# sys.exit(0)

