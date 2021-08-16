from datetime import datetime
import random
import requests, json, sys, time
from .modules import create_temp_json
from .modules import headers as h
# import modules.create_temp_json as create_temp_json
# import modules.headers as h


f = open(f"./data/params/ashbyhq.txt", "r")
companies = [company.strip() for company in f]
f.close()

data = create_temp_json.data

def getJobs(date, url, company, position, location, param):
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
        "company": company,
        "url": url,
        "location": location,
        "source": company,
        "source_url": f"https://jobs.ashbyhq.com/{param}",
        "category": "job"
    })
    print(f"=> ashbyhq: Added {title} for {company}")


def getResults(item, param, name):
    jobs = item["data"]["jobPostingBriefs"]

    for data in jobs:
        if "Engineer" in data["departmentName"] or "Data" in data["departmentName"] or "Data" in data["title"] or "IT " in data["title"] or "Tech" in data["title"] or "Support" in data["title"] and "Electrical" not in data["title"] and "HVAC" not in data["title"] and "Mechnical" not in data["title"]:
            date = datetime.strftime(datetime.now(), "%Y-%m-%d")
            jobId = data["id"].strip()
            apply_url = f"https://jobs.ashbyhq.com/{param}/{jobId}"
            company_name = name
            position = data["title"].strip()
            locations_string = data["locationName"].strip()
            
            getJobs(date, apply_url, company_name, position, locations_string, param)
        

def getURL():
    page = 1

    for company in companies:
        try:
            headers = {"User-Agent": random.choice(h.headers)}
            url = "https://jobs.ashbyhq.com/api/non-user-graphql"
            payload = {
                "operationName":"ApiJobPostingBriefsWithIds",
                "variables":{
                    "organizationHostedJobsPageName":company
                },
                "query":"query ApiJobPostingBriefsWithIds($organizationHostedJobsPageName: String!) {\n  jobPostingBriefs: jobPostingBriefsWithIds(organizationHostedJobsPageName: $organizationHostedJobsPageName) {\n    id\n    title\n    departmentId\n    departmentName\n    locationId\n    locationName\n    employmentType\n    __typename\n  }\n}\n"
            }

            payload2 = {
                "operationName":"ApiOrganizationFromHostedJobsPageName",
                "variables":{
                    "organizationHostedJobsPageName":company
                },
                "query":"query ApiOrganizationFromHostedJobsPageName($organizationHostedJobsPageName: String!) {\n  organization: organizationFromHostedJobsPageName(organizationHostedJobsPageName: $organizationHostedJobsPageName) {\n    ...OrganizationParts\n    __typename\n  }\n}\n\nfragment OrganizationParts on Organization {\n  name\n  publicWebsite\n  customJobsPageUrl\n  theme {\n    colors\n    logoWordmarkImageUrl\n    logoSquareImageUrl\n    applicationSubmittedSuccessMessage\n    jobBoardTopDescriptionHtml\n    jobBoardBottomDescriptionHtml\n    __typename\n  }\n  appConfirmationTrackingPixelHtml\n  __typename\n}\n"
            }

            response = requests.post(url, json=payload, headers=headers).text
            data = json.loads(response)

            res = requests.post(url, json=payload2, headers=headers).text
            name = json.loads(res)["data"]["organization"]["name"]

            getResults(data, company, name)

            if page % 10 == 0:
                time.sleep(5)
                    
            page+=1
        except:
            print(f"Failed to scrape {company}")
            continue
     

def main():
    getURL()

# main()
# sys.exit(0)