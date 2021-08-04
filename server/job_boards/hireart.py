from datetime import datetime
from bs4 import BeautifulSoup
import requests, json, sys
from .modules import create_temp_json
# import modules.create_temp_json as create_temp_json


data = create_temp_json.data

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0"}

def getJobs(url, company, position, location, qualifications):
    date = datetime.strftime(datetime.now(), "%Y-%m-%d")
    title = position
    qualifications = qualifications
    company = company
    url = url
    location = location

    # print(date, title, company, url, location)
    postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d"))
    
    data.append({
        "timestamp": postDate,
        "title": title,
        "qualifications": qualifications,
        "company": company,
        "url": url,
        "location": location,
        "source": "HireArt",
        "source_url": "https://www.hireart.com",
        "category": "job"
    })
    print(f"=> hireart: Added {title} for {company}")


def getResults(item):
    jobs = item["jobs"]
    for data in jobs:
        apply_url = data["apply_url"].strip()
        response = requests.get(apply_url, headers=headers).text
        soup = BeautifulSoup(response, "lxml")
        results = soup.find("div", class_="job-requirements").find_all("li")
        desc = [i.text for i in results]

        company_name = data["company_name"].strip()
        position = data["position"].strip()
        locations_string = data["locations_string"].strip()
        getJobs(apply_url, company_name, position, locations_string, desc)

def getURL():
    url = f"https://www.hireart.com/v1/candidates/browse_jobs?region&job_category=engineering&page=1&per=10000"
    response = requests.get(url, headers=headers)

    if response.ok:
        data = json.loads(response.text)
        getResults(data)
    else:
        print("=> hireart: Error - Response status", response.status_code)
    
    # print(data)
     


def main():
    getURL()

# main()
# sys.exit(0)

