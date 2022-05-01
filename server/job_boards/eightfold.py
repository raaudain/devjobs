import requests
import json
import sys
import time
import random
from datetime import datetime
from .modules import create_temp_json
from .modules import headers as h
from .modules.classes import List_Of_Companies, Page_Not_Found
# import modules.create_temp_json as create_temp_json
# import modules.headers as h
# import modules.classes as c


FILE_PATH = "./data/params/eightfold.txt"


def get_jobs(date: str, url: str, company: str, position: str, location: str, param: str):
    data = create_temp_json.data
    scraped = create_temp_json.scraped
    post_date = datetime.timestamp(
        datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S"))
    data.append({
        "timestamp": post_date,
        "title": position,
        "company": company,
        "url": url,
        "location": location,
        "source": company,
        "source_url": f"https://{param}.eightfold.ai/careers/",
        "category": "job"
    })
    scraped.add(company)
    print(f"=> eightfold.ai: Added {position} for {company}")


def get_results(item: str, param: str):
    jobs = item["positions"]
    company = item["branding"]["companyName"] if "companyName" in item["branding"] else param.upper()
    for j in jobs:
        if "Engineer" in j["name"] or "Data" in j["name"] or "Support" in j["name"] or "IT" in j["name"] or "Programmer" in j["name"] or "QA" in j["name"] or "Software" in j["name"] or "Tech " in j["name"] or "Help" in j["name"] or "Desk" in j["name"] or "Developer" in j["name"] or "Web" in j["name"] and ("Mechnicial" not in j["name"] and "Electrical" not in j["name"] and "Front Desk" not in j["name"] and "Data Entry" not in j["name"] and "Facilities" not in j["name"] and "Nurse" not in j["name"]):
            date = datetime.fromtimestamp(j["t_create"])
            position = j["name"].strip()
            company_name = company.strip()
            apply_url = f"https://{param}.eightfold.ai/careers/?pid={j['id']}"
            locations_string = " | ".join(j["locations"])
            get_jobs(date, apply_url, company_name,
                     position, locations_string, param)


def get_url(companies: list):
    count = 1
    for name in companies:
        headers = {"User-Agent": random.choice(h.headers)}
        url = f"https://{name}.eightfold.ai/api/apply/v2/jobs?start=0&num=1000"
        response = requests.get(url, headers=headers)
        if response.ok:
            data = json.loads(response.text)
            get_results(data, name)
            if count % 15 == 0:
                time.sleep(60)
            count += 1
        elif response.status_code == 404:
            not_found = Page_Not_Found(FILE_PATH, name)
            not_found.remove_not_found()
        else:
            print(
                f"=> eightfold.ai: Status code {response.status_code} for {name}")


def main():
    companies = List_Of_Companies(FILE_PATH).read_file()
    get_url(companies)


# main()
# sys.exit(0)
