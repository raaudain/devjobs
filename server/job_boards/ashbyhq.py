from datetime import datetime
import requests, json, sys, time
from .modules import create_temp_json
# import modules.create_temp_json as create_temp_json


f = open(f"./data/params/ashbyhq.txt", "r")
companies = [company.strip() for company in f]
f.close()

data = create_temp_json.data

def getJobs(date, url, company, position, location):
    date = str(date)
    title = position
    company = company
    url = url
    location = location

    # print(date, title, company, url, location)

    postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d"))
    
    data.append({
        "timestamp": postDate,
        "title": title,
        "company": company.capitalize(),
        "url": url,
        "location": location,
        "source": company.capitalize(),
        "source_url": f"https://jobs.ashbyhq.com/{company}",
        "category": "job"
    })
    print(f"=> ashbyhq: Added {title} for {company}")


def getResults(item, company):
    jobs = item["data"]["jobPostingBriefs"]

    for data in jobs:
        if "Engineer" in data["departmentName"] or "Data" in data["title"] or "IT " in data["title"] or "Tech" in data["title"] or "Support" in data["title"]:
            date = datetime.strftime(datetime.now(), "%Y-%m-%d")
            jobId = data["id"].strip()
            apply_url = f"https://jobs.ashbyhq.com/{company}/{jobId}"
            company_name = company
            position = data["title"].strip()
            locations_string = data["locationName"].strip()
            
            getJobs(date, apply_url, company_name, position, locations_string)
        

def getURL():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"}

    page = 1

    for company in companies:
        url = "https://jobs.ashbyhq.com/api/non-user-graphql"
        payload = {
            "operationName":"ApiJobPostingBriefsWithIds",
            "variables":{
                "organizationHostedJobsPageName":company
            },
            "query":"query ApiJobPostingBriefsWithIds($organizationHostedJobsPageName: String!) {\n  jobPostingBriefs: jobPostingBriefsWithIds(organizationHostedJobsPageName: $organizationHostedJobsPageName) {\n    id\n    title\n    departmentId\n    departmentName\n    locationId\n    locationName\n    employmentType\n    __typename\n  }\n}\n"
        }

        response = requests.post(url, json=payload, headers=headers).text

        data = json.loads(response)

        getResults(data, company)

        if page % 10 == 0:
            time.sleep(5)
                
        
        
        page+=1
    # print(data)
     


def main():
    getURL()

# main()
# sys.exit(0)