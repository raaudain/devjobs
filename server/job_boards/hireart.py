from datetime import datetime
from bs4 import BeautifulSoup
import requests, json, sys, random
from .modules import create_temp_json
from .modules import headers as h
# import modules.create_temp_json as create_temp_json
# import modules.headers as h


data = create_temp_json.data

headers = {"User-Agent": random.choice(h.headers)}

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
        try:
            apply_url = data["apply_url"].strip()
            response = requests.get(apply_url, headers=headers).text
            soup = BeautifulSoup(response, "lxml")
            results = soup.find("div", class_="job-requirements").find_all("li")
            desc = [i.text for i in results]

            company_name = data["company_name"].strip()
            position = data["position"].strip()
            locations_string = data["locations_string"].strip()
            getJobs(apply_url, company_name, position, locations_string, desc)
        except:
            print("Error with hireart")

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

