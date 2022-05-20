import requests
import json
import sys
import time
import random
from datetime import datetime
from bs4 import BeautifulSoup
from .modules import create_temp_json
from .modules import headers as h
from .modules.classes import Filter_Jobs, Read_List_Of_Companies, Remove_Not_Found
# import modules.create_temp_json as create_temp_json
# import modules.headers as h
# import modules.classes as c


FILE_PATH = "./data/params/greenhouse_io.txt"


def get_results(item: str, name: str, company: str, logo: str):
    jobs = item["jobs"]
    if jobs:
        for j in jobs:
            date = datetime.strptime(
                j["updated_at"], "%Y-%m-%dT%H:%M:%S%z")
            post_date = datetime.timestamp(
                datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S%z"))
            position = j["title"].strip()
            company_name = company
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
                "source_url": f"https://boards.greenhouse.io/{name}"
            })


def get_url(companies: list):
    count = 1
    for name in companies:
        try:
            headers = {"User-Agent": random.choice(h.headers)}
            url = f"https://boards-api.greenhouse.io/v1/boards/{name}/jobs"
            url2 = f"https://boards-api.greenhouse.io/v1/boards/{name}/"
            url3 = f"https://boards.greenhouse.io/{name}"
            response = requests.get(url, headers=headers)
            res = requests.get(url2, headers=headers)
            if response.ok and res.ok:
                data = json.loads(response.text)
                company = json.loads(res.text)["name"].strip()
                logo = None
                if name != "intersystems":
                    try:
                        r = requests.get(url3, headers=headers)
                        soup = BeautifulSoup(r.text, "lxml")
                        logo = soup.find(id="logo").find("img")[
                            "src"] if soup.find(id="logo") else None
                    except:
                        print(
                            f"=> greenhouse.io: Error getting logo for {name}.")
                if data and company:
                    get_results(data, name, company, logo)
                if count % 20 == 0:
                    time.sleep(10)
                else:
                    time.sleep(0.2)
                count += 1
            elif response.status_code == 404:
                Remove_Not_Found(FILE_PATH, name)
            else:
                print(
                    f"=> greenhouse.io: Status code {response.status_code} for {name}")
        except:
            print(f"Error for {name}.")


def main():
    companies = Read_List_Of_Companies(FILE_PATH)
    get_url(companies)


# main()
# sys.exit(0)
