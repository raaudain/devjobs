import requests
import sys
import json
import time
import random
from datetime import datetime
from lxml import html
from .helpers import headers as h
from .helpers.classes import Filter_Jobs, Get_Stored_Data, Remove_Not_Found, Read_List_Of_Companies
# import modules.headers as h
# import modules.classes as c


FILE_PATH = "./data/params/lever_co.txt"


def get_results(item: str, param: str):
    source_url = f"https://jobs.lever.co/{param}"
    company_name = param.capitalize()
    logo = None
    lever = "./data/assets/lever_assets.txt"
    table = Get_Stored_Data(lever)
    if param in table:
        company_name = table[param]["name"] 
        logo = table[param]["logo"]
    else:
        try:
            r = requests.get(source_url)
            tree = html.fromstring(r.content)
            logo = tree.xpath("//a[@class='main-header-logo']/img/@src")[0]
            company_name = tree.xpath("//head/title/text()")[0]
            with open(lever, "a") as a:
                a.write(f"{param}`{company_name}`{logo}\n")
        except Exception as e:
            print(f"=> lever.co: Failed to get logo for {param}. Error: {e}.")
    for i in item:
        # use true division by 1e3 (float 1000)
        date = datetime.fromtimestamp(i["createdAt"] / 1e3)
        post_date = datetime.timestamp(
            datetime.strptime(str(date).rsplit(".")[0], "%Y-%m-%d %H:%M:%S"))
        apply_url = i["hostedUrl"].strip()
        description = i["descriptionPlain"]
        position = i["text"].strip()
        location = i["categories"]["location"].strip() if "location" in i["categories"] else "See description"
        Filter_Jobs({
            "timestamp": post_date,
            "title": position,
            "company": company_name,
            "company_logo": logo,
            #"description": description,
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
                    time.sleep(0.2)
            elif response.status_code == 404:
                Remove_Not_Found(FILE_PATH, company)
            count += 1
        except Exception as e:
            if response.status_code == 429:
                print(
                    f"=> lever.co: Failed to scrape {company}. Status code: {response.status_code}.")
                break
            else:
                print(
                    f"=> lever.co: Failed for {company}. Status code: {response.status_code}. Error: {e}.")


def main():
    companies = Read_List_Of_Companies(FILE_PATH)
    get_url(companies)


# main()
# sys.exit(0)
