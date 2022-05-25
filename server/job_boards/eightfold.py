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


FILE_PATH = "./data/params/eightfold.txt"


def get_results(item: str, param: str):
    jobs = item["positions"]
    company = item["branding"]["companyName"] if "companyName" in item["branding"] else param.upper()
    for j in jobs:
        date = datetime.fromtimestamp(j["t_create"])
        post_date = datetime.timestamp(
            datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S"))
        position = j["name"].strip()
        company_name = company.strip()
        description = j["job_description"]
        department = j["department"]
        apply_url = f"https://{param}.eightfold.ai/careers/?pid={j['id']}"
        location = " | ".join(j["locations"])
        Filter_Jobs({
            "timestamp": post_date,
            "title": position,
            "company": company_name,
            #"description": description,
            "department": department,
            "url": apply_url,
            "location": location,
            "source": company_name,
            "source_url": f"https://{param}.eightfold.ai/careers/"
        })


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
            else:
                time.sleep(0.2)
            count += 1
        elif response.status_code == 404:
            Remove_Not_Found(FILE_PATH, name)
        else:
            print(
                f"=> eightfold.ai: Status code {response.status_code} for {name}")


def main():
    companies = Read_List_Of_Companies(FILE_PATH)
    get_url(companies)


# main()
# sys.exit(0)
