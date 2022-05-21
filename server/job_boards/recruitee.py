from datetime import datetime
import requests
import json
import sys
import time
import random
from lxml import html
from .modules.classes import Filter_Jobs, Read_List_Of_Companies, Remove_Not_Found
from .modules import headers as h
# import modules.headers as h
# import modules.classes as c


FILE_PATH = "./data/params/recruitee.txt"


def get_results(item: str, param: str):
    jobs = item["offers"]
    source_url = f"https://{param}.recruitee.com"
    r = requests.get(source_url)
    tree = html.fromstring(r.content)
    img = tree.xpath("//img/@src")[0]
    logo = img if img else None
    for job in jobs:
        date = datetime.strptime(job["published_at"], "%Y-%m-%d %H:%M:%S UTC")
        post_date = datetime.timestamp(
            datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S"))
        apply_url = job["careers_url"].strip()
        company_name = job["company_name"].strip()
        position = job["title"].strip()
        description = job["description"]
        location = job["location"].strip()
        Filter_Jobs({
            "timestamp": post_date,
            "title": position,
            "company": company_name,
            "company_logo": logo,
            "description": description,
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
            url = f"https://{company}.recruitee.com/api/offers/"
            response = requests.get(url, headers=headers)
            if response.status_code == 404:
                Remove_Not_Found(FILE_PATH, company)
            data = json.loads(response.text)
            get_results(data, company)
            if count % 20 == 0:
                time.sleep(10)
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
                    f"=> workable: Failed for {company}. Status code: {response.status_code}. Error: {e}")


def main():
    companies = Read_List_Of_Companies(FILE_PATH)
    get_url(companies)


# main()
# sys.exit(0)
