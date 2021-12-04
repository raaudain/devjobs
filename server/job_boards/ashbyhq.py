import requests, json, sys, time, random
from datetime import datetime
from .modules import create_temp_json
from .modules import headers as h
from .modules.classes import Page_Not_Found
# import modules.create_temp_json as create_temp_json
# import modules.headers as h


def get_jobs(date: str, url: str, company: str, position: str, location: str, logo: str, param: str):
    data = create_temp_json.data
    scraped = create_temp_json.scraped

    post_date = datetime.timestamp(datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S"))
    
    data.append({
        "timestamp": post_date,
        "title": position,
        "company": company,
        "company_logo": logo,
        "url": url,
        "location": location,
        "source": company,
        "source_url": f"https://jobs.ashbyhq.com/{param}",
        "category": "job"
    })
    scraped.add(company)
    print(f"=> ashbyhq: Added {position} for {company}")


def get_results(item: str, param: str, name: str, logo: str):
    jobs = item["data"]["jobPostingBriefs"]

    for data in jobs:
        if "Engineer" in data["departmentName"] or "Data" in data["departmentName"] or "Data" in data["title"] or "IT " in data["title"] or "Tech" in data["title"] or "Support" in data["title"] or "Engineer" in data["title"] or "Developer" in data["title"] and ("Electrical" not in data["title"] and "HVAC" not in data["title"] and "Mechnical" not in data["title"]):
            date = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
            job_id = data["id"].strip()
            apply_url = f"https://jobs.ashbyhq.com/{param}/{job_id}"
            company_name = name
            position = data["title"].strip()
            locations_string = data["locationName"].strip()
            
            get_jobs(date, apply_url, company_name, position, locations_string, logo, param)


def get_url(companies: list):
    page = 1

    for company in companies:
        headers = {"User-Agent": random.choice(h.headers)}
        url = "https://jobs.ashbyhq.com/api/non-user-graphql"
        payload = {
            "operationName":"ApiJobPostingBriefsWithIds",
            "variables":{
                "organizationHostedJobsPageName":company
            },
            "query":"query ApiJobPostingBriefsWithIds($organizationHostedJobsPageName: String!) {\n  jobPostingBriefs: jobPostingBriefsWithIds(organizationHostedJobsPageName: $organizationHostedJobsPageName) {\n    id\n    title\n    departmentId\n    departmentName\n    locationId\n    locationName\n    employmentType\n    __typename\n  }\n}\n"
        }
        payload_2 = {
            "operationName":"ApiOrganizationFromHostedJobsPageName",
            "variables":{
                "organizationHostedJobsPageName":company
            },
            "query":"query ApiOrganizationFromHostedJobsPageName($organizationHostedJobsPageName: String!) {\n  organization: organizationFromHostedJobsPageName(organizationHostedJobsPageName: $organizationHostedJobsPageName) {\n    ...OrganizationParts\n    __typename\n  }\n}\n\nfragment OrganizationParts on Organization {\n  name\n  publicWebsite\n  customJobsPageUrl\n  theme {\n    colors\n    logoWordmarkImageUrl\n    logoSquareImageUrl\n    applicationSubmittedSuccessMessage\n    jobBoardTopDescriptionHtml\n    jobBoardBottomDescriptionHtml\n    __typename\n  }\n  appConfirmationTrackingPixelHtml\n  __typename\n}\n"
        }
        response = requests.post(url, json=payload, headers=headers)
        res = requests.post(url, json=payload_2, headers=headers)

        if response.ok and res.ok:
            data = json.loads(response.text)
            name = None
            logo = None

            if json.loads(res.text)["data"]["organization"]:
                try:
                    name = json.loads(res.text)["data"]["organization"]["name"]
                    logo = json.loads(res.text)["data"]["organization"]["theme"]["logoWordmarkImageUrl"] if json.loads(res.text)["data"]["organization"]["theme"] else None
                except TypeError as err:
                    print(f"=> ashbyhq: Error for {company}.", err)
            else:
                not_found = Page_Not_Found("./data/params/ashbyhq.txt", company)
                not_found.remove_unwanted()

            get_results(data, company, name, logo)
            if page % 10 == 0: time.sleep(5)   
            page+=1
        else:
            print(f"=> ashbyhq: Failed to scrape {company}. Status codes: {response.status_code} and {res.status_code}.")


def main():
    f = open(f"./data/params/ashbyhq.txt", "r")
    companies = [company.strip() for company in f]
    f.close()

    get_url(companies)

# main()
# sys.exit(0)