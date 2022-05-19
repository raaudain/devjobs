import requests
import json
import sys
import time
import random
from datetime import datetime
from .modules import create_temp_json
from .modules import headers as h
from .modules.classes import Read_List_Of_Companies, Remove_Not_Found, Filter_Jobs
# import modules.create_temp_json as create_temp_json
# import modules.headers as h
# import modules.classes as c


FILE_PATH = "./data/params/ashbyhq.txt"


def get_results(item: str, param: str, name: str, logo: str):
    jobs = item["data"]["jobPostingBriefs"]
    for data in jobs:
        date = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
        post_date = datetime.timestamp(
            datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S"))
        job_id = data["id"].strip()
        apply_url = f"https://jobs.ashbyhq.com/{param}/{job_id}"
        company_name = name
        position = data["title"].strip()
        locations_string = data["locationName"].strip()
        source_url = f"https://jobs.ashbyhq.com/{param}"
        Filter_Jobs({
            "timestamp": post_date,
            "title": position,
            "company": company_name,
            "company_logo": logo,
            "url": apply_url,
            "location": locations_string,
            "source": company_name,
            "source_url": source_url,
        })


def get_url(companies: list):
    page = 1
    for company in companies:
        headers = {"User-Agent": random.choice(h.headers)}
        url = "https://jobs.ashbyhq.com/api/non-user-graphql"
        payload = {
            "operationName": "ApiJobPostingBriefsWithIds",
            "variables": {
                "organizationHostedJobsPageName": company
            },
            "query": "query ApiJobPostingBriefsWithIds($organizationHostedJobsPageName: String!) {\n  jobPostingBriefs: jobPostingBriefsWithIds(organizationHostedJobsPageName: $organizationHostedJobsPageName) {\n    id\n    title\n    departmentId\n    departmentName\n    locationId\n    locationName\n    employmentType\n    __typename\n  }\n}\n"
        }
        payload_2 = {
            "operationName": "ApiOrganizationFromHostedJobsPageName",
            "variables": {
                "organizationHostedJobsPageName": company
            },
            "query": "query ApiOrganizationFromHostedJobsPageName($organizationHostedJobsPageName: String!) {\n  organization: organizationFromHostedJobsPageName(organizationHostedJobsPageName: $organizationHostedJobsPageName) {\n    ...OrganizationParts\n    __typename\n  }\n}\n\nfragment OrganizationParts on Organization {\n  name\n  publicWebsite\n  customJobsPageUrl\n  theme {\n    colors\n    logoWordmarkImageUrl\n    logoSquareImageUrl\n    applicationSubmittedSuccessMessage\n    jobBoardTopDescriptionHtml\n    jobBoardBottomDescriptionHtml\n    __typename\n  }\n  appConfirmationTrackingPixelHtml\n  __typename\n}\n"
        }
        response = requests.post(url, json=payload, headers=headers)
        res = requests.post(url, json=payload_2, headers=headers)
        if response.ok and res.ok:
            data = json.loads(response.text)
            name = None
            logo = None
            if "organization" in json.loads(res.text)["data"]:
                try:
                    name = json.loads(res.text)["data"]["organization"]["name"]
                    logo = json.loads(res.text)["data"]["organization"]["theme"]["logoWordmarkImageUrl"] if json.loads(
                        res.text)["data"]["organization"]["theme"] else None
                except TypeError as err:
                    print(f"=> ashbyhq: Error for {company}.", err)
            else:
                Remove_Not_Found(FILE_PATH, company)
            get_results(data, company, name, logo)
            if page % 10 == 0:
                time.sleep(5)
            else:
                time.sleep(0.05)
            page += 1
        else:
            print(
                f"=> ashbyhq: Failed to scrape {company}. Status codes: {response.status_code} and {res.status_code}.")


def main():
    companies = Read_List_Of_Companies(FILE_PATH)
    get_url(companies)


# main()
# sys.exit(0)
