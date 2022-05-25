import requests
import json
import sys
import time
import random
from lxml import html
from datetime import datetime
from .modules import headers as h
from .modules.classes import Filter_Jobs, Get_Stored_Data, Read_List_Of_Companies, Remove_Not_Found
# import modules.headers as h
# import modules.classes as c


FILE_PATH = "./data/params/eightfold.txt"


def get_results(item: str, param: str):
    jobs = item["positions"]
    company_name = item["branding"]["companyName"].strip(
    ) if "companyName" in item["branding"] else param.capitalize()
    logo = None
    source_url = f"https://{param}.eightfold.ai/careers/"
    ef = "./data/assets/eightfold_assets.txt"
    table = Get_Stored_Data(ef)
    if param in table:
        logo = table[param]["logo"]
    else:
        try:
            r = requests.get(source_url)
            tree = html.fromstring(r.content)
            logo = tree.xpath(
                "//img[@class='d-inline-block align-top']/@src")[0]
            with open(ef, "a") as a:
                a.write(f"{param}`n/a`{logo}\n")
        except Exception as e:
            print(f"=> eightfold.ai: Error getting logo for {param}. {e}.")
    for j in jobs:
        date = datetime.fromtimestamp(j["t_create"])
        post_date = datetime.timestamp(
            datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S"))
        position = j["name"].strip()
        description = j["job_description"]
        department = j["department"]
        apply_url = f"https://{param}.eightfold.ai/careers/?pid={j['id']}"
        location = " | ".join(j["locations"])
        Filter_Jobs({
            "timestamp": post_date,
            "title": position,
            "company": company_name,
            "company_logo": logo,
            # "description": description,
            # "department": department,
            "url": apply_url,
            "location": location,
            "source": company_name,
            "source_url": source_url
        })


def get_url(companies: list):
    count = 1
    for company in companies:
        try:
            headers = {"User-Agent": random.choice(h.headers)}
            url = f"https://{company}.eightfold.ai/api/apply/v2/jobs?start=0&num=1000"
            response = requests.get(url, headers=headers)
            if response.ok:
                data = json.loads(response.text)
                get_results(data, company)
                if count % 15 == 0:
                    time.sleep(60)
                else:
                    time.sleep(0.2)
                count += 1
            elif response.status_code == 404:
                Remove_Not_Found(FILE_PATH, company)
            else:
                print(
                    f"=> eightfold.ai: Status code {response.status_code} for {company}.")
        except Exception as e:
            print(f"=> eightfold.ai: Error for {company}. {e}.")


def main():
    companies = Read_List_Of_Companies(FILE_PATH)
    get_url(companies)


# main()
# sys.exit(0)
