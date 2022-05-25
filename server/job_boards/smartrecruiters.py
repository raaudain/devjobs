from posixpath import split
import requests
import sys
import json
import time
import random
from datetime import datetime
from lxml import html
from .modules import headers as h
from .modules.classes import Filter_Jobs, Get_Stored_Data, Read_List_Of_Companies, Remove_Not_Found
# import modules.headers as h
# import modules.classes as c


FILE_PATH = "./data/params/smartrecruiters.txt"


def get_results(item: str, param: str):
    data = item["content"]
    sr = "./data/assets/smartrecruiters_assets.txt"
    table = Get_Stored_Data(sr)
    logo = None
    if param in table:
        logo = table[param]["logo"]
    if data:
        for i in data:
            date = datetime.strptime(
                i["releasedDate"], "%Y-%m-%dT%H:%M:%S.%fZ")
            post_date = datetime.timestamp(
                datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S"))
            jobId = i["id"]
            company_name = i["company"]["name"]
            apply_url = f"https://jobs.smartrecruiters.com/{param}/{jobId}"
            position = i["name"]
            if logo == None:
                try:
                    if ("Engineer" in position or "Data" in position or "IT " in position or "Tech " in position or "QA" in position or "Programmer" in position or "Developer" in position or "ML" in position or "SDET" in position or "devops" in position.lower() or "AWS" in position or "Cloud" in position or "Software" in position or "Help" in position or "Web " in position or "Front End" in position or "Agile" in position and "Cyber" in position) and ("Elect" not in position and "HVAC" not in position and "Mechanical" not in position and "Manufactur" not in position and "Data Entry" not in position and "Nurse" not in position and "Maintenance" not in position and "Civil" not in position and "Environmental" not in position and "Hardware" not in position and "Front Desk" not in position and "Helper" not in position and "Peer Support" not in position and "Bridge" not in position and "Water" not in position and "Dispatch" not in position and "Saw" not in position and "Facilities" not in position and "AML" not in position and "Sheet Metal" not in position and "Metallurgical" not in position and "Materials" not in position):
                        r = requests.get(apply_url)
                        tree = html.fromstring(r.content)
                        logo = tree.xpath(
                            "//img[contains(@src, 'https://c.smartrecruiters.com/sr-company-logo')]/@src")[0].rsplit("&")[0]
                        with open(sr, "a") as a:
                            a.write(f"{param}`n/a`{logo}\n")
                        table[param] = {"name": "n/a", "logo": logo}
                except Exception as e:
                    print(f"=> smartrecruiter: Error getting logo. {e}.")
            city = f'{i["location"]["city"]}, '
            region = f'{i["location"]["region"]}, ' if "region" in i["location"] else ""
            country = i["location"]["country"].upper()
            remote = " | Remote" if i["location"]["remote"] else ""
            location = f"{city}{region}{country}{remote}"
            Filter_Jobs({
                "timestamp": post_date,
                "title": position,
                "company": company_name,
                "company_logo": logo,
                "url": apply_url,
                "location": location,
                "source": company_name,
                "source_url": f"https://careers.smartrecruiters.com/{param}/",
                "category": "job"
            })
    else:
        print(f"=> smartrecruiters: No jobs for {param}.")


def get_url(companies: list):
    count = 1
    for company in companies:
        try:
            headers = {"User-Agent": random.choice(h.headers)}
            url = f"https://api.smartrecruiters.com/v1/companies/{company}/postings/"
            response = requests.get(url, headers=headers)
            if response.ok:
                data = json.loads(response.text)
                get_results(data, company)
                if count % 20 == 0:
                    time.sleep(5)
                else:
                    time.sleep(0.2)
                count += 1
            elif response.status_code == 404:
                Remove_Not_Found(FILE_PATH, company)
        except Exception as e:
            if response.status_code == 429:
                print(
                    f"=> smartrecruiters: Failed to scraped {company}. Status code: {response.status_code}.")
                break
            else:
                print(
                    f"=> smartrecruiters: Failed to scraped {company}. Error: {e}.")


def main():
    companies = Read_List_Of_Companies(FILE_PATH)
    get_url(companies)


# main()
# sys.exit(0)
