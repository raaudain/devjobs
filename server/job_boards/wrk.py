import requests
import json
import sys
import time
import random
from datetime import datetime
from .modules import create_temp_json
from .modules import headers as h
from .modules.classes import Filter_Jobs, Read_List_Of_Companies, Remove_Not_Found
# import modules.create_temp_json as create_temp_json
# import modules.headers as h
# import modules.classes as c


FILE_PATH = "./data/params/wrk.txt"


def get_jobs(date: str, url: str, company: str, position: str, location: str, name: str):
    data = create_temp_json.data
    scraped = create_temp_json.scraped

    post_date = datetime.timestamp(
        datetime.strptime(str(date), "%Y-%m-%dT%H:%M:%S.%fZ"))

    data.append({
        "timestamp": post_date,
        "title": position,
        "company": company,
        "company_logo": None,
        "url": url,
        "location": location,
        "source": company,
        "source_url": f"https://jobs.wrk.xyz/{name}",
        "category": "job"
    })
    scraped.add(company)
    print(f"=> wrk: Added {position} for {company}")


def get_results(item: str, name: str):
    jobs = item["items"]
    if jobs:
        for j in jobs:
            # if "Engineer" in j["title"] or "Data" in j["title"] or "Support" in j["title"] or "IT " in j["title"] or "Programmer" in j["title"] or "QA" in j["title"] or "Software" in j["title"] or "Tech " in j["title"] or "Help" in j["title"] or "Desk" in j["title"] or "Developer" in j["title"] and ("Mechnicial" not in j["title"] and "Electrical" not in j["title"] and "Front Desk" not in j["title"]):
            date = j["published_at"]
            post_date = datetime.timestamp(
                datetime.strptime(str(date), "%Y-%m-%dT%H:%M:%S.%fZ"))
            position = j["title"].strip()
            company_name = j["organization_name"].strip()
            apply_url = j["job_post_url"].strip()
            city = f"{j['city'].strip()}, " if j['city'] else ""
            state = f"{j['state_region'].strip()}, " if j["state_region"] else ""
            country = f"{j['country'].strip()}" if j["country"] else ""
            remote = f" | {j['remoteness_pretty'].strip()}" if j["remoteness_pretty"] and "No" not in j["remoteness_pretty"] else ""
            location = city+state+country+remote
            Filter_Jobs({
                "timestamp": post_date,
                "title": position,
                "company": company_name,
                "company_logo": None,
                "url": apply_url,
                "location": location,
                "source": company_name,
                "source_url": f"https://jobs.wrk.xyz/{name}"
            })
            # get_jobs(date, apply_url, company_name,
            #             position, locations_string, name)


def get_url(companies: list):
    count = 1
    for name in companies:
        try:
            headers = {"User-Agent": random.choice(h.headers)}
            url = f"https://jobs.wrk.xyz/api/v1/public/organizations/{name}/jobs/"
            response = requests.get(url, headers=headers)
            if response.ok:
                data = json.loads(response.text)
                get_results(data, name)
                if count % 20 == 0:
                    time.sleep(5)
                count += 1
            elif response.status_code == 404:
                Remove_Not_Found(FILE_PATH, name)
            else:
                print(f"=> wrk: Status code {response.status_code} for {name}")
        except:
            print(f"=> wrk: Error for {name}.")


def main():
    companies = Read_List_Of_Companies(FILE_PATH)
    get_url(companies)


# main()
# sys.exit(0)
