import requests
import sys
import json
import time
import random
from datetime import datetime
from lxml import html
from .modules import headers as h
from .modules.classes import Filter_Jobs, Remove_Not_Found, Read_List_Of_Companies
# import modules.headers as h
# import modules.classes as c


FILE_PATH = "./data/params/lever_co.txt"


def get_results(item, param):
    source_url = f"https://jobs.lever.co/{param}"
    r = requests.get(source_url)
    tree = html.fromstring(r.content)
    img = tree.xpath("//a[@class='main-header-logo']/img/@src")[0]
    company = tree.xpath("//head/title/text()")[0]
    company_name = company if company else param.capitalize()
    logo = img if img else None
    for i in item:
        # use true division by 1e3 (float 1000)
        date = datetime.fromtimestamp(i["createdAt"] / 1e3)
        post_date = datetime.timestamp(
            datetime.strptime(str(date)[:-7], "%Y-%m-%d %H:%M:%S"))
        apply_url = i["hostedUrl"].strip()
        position = i["text"].strip()
        location = i["categories"]["location"].strip()
        Filter_Jobs({
            "timestamp": post_date,
            "title": position,
            "company": company_name,
            "company_logo": logo,
            "url": apply_url,
            "location": location,
            "source": company_name,
            "source_url": source_url
        })


def get_url(companies: list):
    count = 0
    for company in companies:
        try:
            headers = {"User-Agent": random.choice(h.headers)}
            url = f"https://api.lever.co/v0/postings/{company}/"
            response = requests.get(url, headers=headers)
            if response.ok:
                data = json.loads(response.text)
                get_results(data, company)
                if count % 20 == 0:
                    time.sleep(10)
                else:
                    time.sleep(0.05)
            elif response.status_code == 404:
                Remove_Not_Found(FILE_PATH, company)
            count += 1
        except:
            if response.status_code == 429:
                print(
                    f"=> lever.co: Failed to scrape {company}. Status code: {response.status_code}.")
                break
            else:
                print(
                    f"=> lever.co: Failed for {company}. Status code: {response.status_code}.")


def main():
    companies = Read_List_Of_Companies(FILE_PATH)
    get_url(companies)


# main()
# sys.exit(0)
