from datetime import datetime, timedelta
import requests, json, sys, time
from .modules import create_temp_json
# import modules.create_temp_json as create_temp_json


data = create_temp_json.data
scraped = create_temp_json.scraped

jobs = ["developer", "software engineer", "devops", "support engineer", "frontend", "backend", "fullstack", "it engineer", "desktop support", "helpdesk", "it support", "qa analyst", "cloud", "network", "security", "qa tester", "database", "software"]

def getJobs(date, url, company, position, location, logo):
    # age = datetime.timestamp(datetime.now() - timedelta(days=7))
    post_date = datetime.timestamp(datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S"))
    
    if url not in scraped and company not in scraped:
        data.append({
            "timestamp": post_date,
            "title": position,
            "company": company,
            "company_logo": logo,
            "url": url,
            "location": location,
            "source": "Dice",
            "source_url": "https://www.dice.com",
            "category": "job"
        })
        print(f"=> dice: Added {position} for {company}")
        scraped.add(url)
            

def getResults(item):
    data = item["data"]
    recruiters = ("VDart, Inc.", "Net2Source Inc.", "Sumeru")

    for d in data:
        if d["companyName"] not in recruiters:
            date = datetime.strptime(d["postedDate"], "%Y-%m-%dT%H:%M:%SZ")
            position = d["title"].strip()
            company_name = d["companyName"].strip()
            logo = "https:"+d["companyLogoUrl"].strip() if "companyLogoUrl" in d else None
            apply_url = d["detailsPageUrl"].strip()
            locations_string = d["jobLocation"]["displayName"].strip() if "jobLocation" in d else None

            getJobs(date, apply_url, company_name, position, locations_string, logo)


def getURL():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36", "X-Api-Key": "1YAt0R9wBg4WfsF9VB2778F5CHLAPMVW3WAZcKd8", "Origin": "https://www.dice.com"}

    for job in jobs:
        try:
            url = f"https://job-search-api.svc.dhigroupinc.com/v1/dice/jobs/search?q={job}&countryCode2=US&radius=30&radiusUnit=mi&page=1&pageSize=1000&facets=employmentType%7CpostedDate%7CworkFromHomeAvailability%7CemployerType%7CeasyApply%7CisRemote&filters.employerType=Direct%20Hire&filters.postedDate=SEVEN&fields=id%7CjobId%7Csummary%7Ctitle%7CpostedDate%7CjobLocation.displayName%7CdetailsPageUrl%7Csalary%7CclientBrandId%7CcompanyPageUrl%7CcompanyLogoUrl%7CpositionId%7CcompanyName%7CemploymentType%7CisHighlighted%7Cscore%7CeasyApply%7CemployerType%7CworkFromHomeAvailability%7CisRemote&culture=en&recommendations=true&interactionId=0&fj=true&includeRemote=true"

            response = requests.get(url, headers=headers).text
            data = json.loads(response)

            getResults(data)
            # print(data)
            time.sleep(5)

        except:
            print("=>  dice: Error for", job)

def main():
    getURL()

# main()
# sys.exit(0)