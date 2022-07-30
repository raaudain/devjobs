import requests
import json
import sys
import time
import random
from datetime import datetime
from bs4 import BeautifulSoup
from .helpers import headers as h
from .helpers.classes import Filter_Jobs, Get_Stored_Data, Read_List_Of_Companies, Remove_Not_Found
# import modules.headers as h
# import modules.classes as c


FILE_PATH = "./data/params/greenhouse_io.txt"


def get_results(item: str, param: str):
    source_url = f"https://boards.greenhouse.io/{param}"
    gh = "./data/assets/greenhouse_assets.txt"
    company_name = param.capitalize()
    logo = None
    jobs = item["jobs"]
    table = Get_Stored_Data(gh)
    if param in table:
        company_name = table[param]["name"]
        logo = table[param]["logo"]
    else:
        try:
            res = requests.get(
                f"https://boards-api.greenhouse.io/v1/boards/{param}/")
            company_name = json.loads(res.text)["name"].strip(
            ) if "name" in json.loads(res.text) else param.capitalize()
            r = requests.get(source_url)
            soup = BeautifulSoup(r.text, "lxml")
            logo = soup.find(id="logo").find("img")[
                "src"].rsplit("?")[0] if soup.find(id="logo") else None
            with open(gh, "a") as a:
                a.write(f"{param}`{company_name}`{logo}\n")
        except Exception as e:
            print(
                f"=> greenhouse.io: Error getting logo for {param}. {e}.")
    for j in jobs:
        date = datetime.strptime(
            j["updated_at"], "%Y-%m-%dT%H:%M:%S%z")
        post_date = datetime.timestamp(
            datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S%z"))
        position = j["title"].strip()
        apply_url = j["absolute_url"].strip()
        location = j["location"]["name"].strip()
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
    count = 1
    for company in companies:
        try:
            headers = {"User-Agent": random.choice(h.headers)}
            url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs"
            response = requests.get(url, headers=headers)
            if response.ok:
                data = json.loads(response.text)
                if data:
                    get_results(data, company)
            elif response.status_code == 404:
                Remove_Not_Found(FILE_PATH, company)
            else:
                print(
                    f"=> greenhouse.io: Status code {response.status_code} for {company}")
            if count % 20 == 0:
                time.sleep(10)
            else:
                time.sleep(0.2)
            count += 1
        except Exception as e:
            print(f"=> greenhouse.io: Error for {company}. {e}.")


def main():
    companies = Read_List_Of_Companies(FILE_PATH)
    get_url(companies)


# main()
# sys.exit(0)
