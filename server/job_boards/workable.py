from datetime import datetime
import requests
import json
import sys
import time
import random
from .modules.classes import Filter_Jobs, Read_List_Of_Companies, Remove_Not_Found
from .modules import headers as h
from .modules import create_temp_json
# import modules.create_temp_json as create_temp_json
# import modules.headers as h
# import modules.classes as c


FILE_PATH = "./data/params/workable.txt"


def get_results(item: str, param: str, company: str, logo: str):
    jobs = item["results"]
    for data in jobs:
        date = datetime.strptime(data["published"], "%Y-%m-%dT%H:%M:%S.%fZ")
        postDate = datetime.timestamp(
            datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S"))
        apply_url = f"https://apply.workable.com/{param}/j/{data['shortcode']}/"
        company_name = company.strip()
        position = data["title"].strip()
        state = f"{data['location']['city']}, {data['location']['region']}, "
        location = f"{state if data['location']['city'] else ''}{data['location']['country']}"
        source_url = f"https://apply.workable.com/{param}/"
        Filter_Jobs({
            "timestamp": postDate,
            "title": position,
            "company": company_name,
            "company_logo": logo,
            "url": apply_url,
            "location": location,
            "source": company_name,
            "source_url": source_url,
        })


def get_url(companies: list):
    count = 0
    retries = 0
    for company in companies:
        token = "0"
        try:
            while token:
                headers = {"User-Agent": random.choice(h.headers)}
                url = f"https://apply.workable.com/api/v3/accounts/{company}/jobs"
                url2 = f"https://apply.workable.com/api/v1/accounts/{company}"
                payload = {
                    "query": "engineer, developer",
                    "location": [],
                    "department": [],
                    "worktype": [],
                    "remote": [],
                    "token": token
                }
                response = requests.post(url, json=payload, headers=headers)
                if response.status_code == 404:
                    Remove_Not_Found(FILE_PATH, company)
                info = requests.get(url2, headers=headers).text
                data = json.loads(response.text)
                # Add name and logo to dictionary to reduce requests
                info_dict = {}
                info_dict[company] = {"name": None, "logo": None}
                name = None
                logo = None
                if info_dict[company]["name"]:
                    name = info_dict[company]["name"]
                    print(f"=> workable: used name in dictionary for {company}")
                else:
                    name = json.loads(info)["name"].strip()
                    info_dict[company]["name"] = name
                if info_dict[company]["logo"]:
                    print(f"=> workable: used logo in dictionary for {company}")
                    logo = info_dict[company]["logo"]
                else:
                    logo = json.loads(info)["logo"] if "logo" in json.loads(
                    info) else None
                    info_dict[company]["logo"] = logo
                get_results(data, company, name, logo)
                token = data["nextPage"] if "nextPage" in data else ""
                if count % 20 == 0:
                    time.sleep(60)
                count += 1
        except:
            if response.status_code == 429:
                print(
                    f"=> workable: Failed to scrape {company}. Status code: {response.status_code}.")
                if retries <= 3:
                    time.sleep(120)
                    retries += 1
                else:
                    print(
                        f"=> workable: Failed to scrape {company}. Status code: {response.status_code}.")
                    break
            else:
                print(
                    f"=> workable: Failed for {company}. Status code: {response.status_code}.")


def main():
    companies = Read_List_Of_Companies(FILE_PATH)
    get_url(companies)


# main()
# sys.exit(0)
