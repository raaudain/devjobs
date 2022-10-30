import requests
import json
import sys
import time
import random
from datetime import datetime
sys.path.insert(0, ".")
from server.job_boards.helpers.classes import ProcessCompanyJobData
from server.job_boards.helpers import headers as h
# import modules.headers as h
# import modules.classes as c


process_data = ProcessCompanyJobData()
FILE_PATH = "server/data/params/workable.txt"


def get_results(item: str, param: str):
    company = item["name"]
    jobs = item["jobs"]
    workable_imgs = "server/data/assets/workable_imgs.txt"
    logo: None
    source_url = f"https://apply.workable.com/{param}/"
    table = process_data.get_stored_data(workable_imgs)
    if param in table:
        logo = table[param]["logo"]
    else:
        r = requests.get(f"https://apply.workable.com/api/v1/accounts/{param}").text
        logo = json.loads(r)["logo"] if "logo" in json.loads(r) else None
        with open(workable_imgs, "a") as a:
            a.write(f"{param}`n/a`{logo}\n")
    for job in jobs:
        date = datetime.strptime(job["published_on"], "%Y-%m-%d")
        post_date = datetime.timestamp(
            datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S"))
        apply_url = job["url"].strip()
        company_name = company.strip()
        position = job["title"].strip()
        description = job["description"]
        remote = "Remote" if job["telecommuting"] else ""
        country = f"{job['country']}" if len(job["country"]) > 0 else ""
        city = f"{job['city']}" if len(job["city"]) > 0 else ""
        state = f"{job['state']}" if len(job["state"]) > 0 else ""
        location = f"{city} {state} {country} {remote}".strip()
        process_data.filter_jobs({
            "timestamp": post_date,
            "title": position,
            "company": company_name,
            "company_logo": logo,
            #"description": description,
            "url": apply_url,
            "location": location,
            "source": company_name,
            "source_url": source_url,
        })


def get_url(companies: list):
    count = 0
    for company in companies:
        try:
            headers = {"User-Agent": random.choice(h.headers)}
            url = f"https://www.workable.com/api/accounts/{company}?details=true"
            response = requests.get(url, headers=headers)
            if response.status_code == 404:
                process_data.remove_not_found(FILE_PATH, company)
            data = json.loads(response.text)
            get_results(data, company)
            if count % 9 == 0:
                time.sleep(15)
            else:
                time.sleep(0.2)
            count += 1
        except Exception as e:
            if response.status_code == 429:
                print(
                    f"=> workable: Failed to scrape {company}. Status code: {response.status_code}.")
                break
            else:
                print(
                    f"=> workable: Failed for {company}. Status code: {response.status_code}. Error: {e}.")


def main():
    companies = process_data.read_list_of_companies(FILE_PATH)
    get_url(companies)


# main()
# sys.exit(0)
