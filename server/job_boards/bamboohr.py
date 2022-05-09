import requests
import sys
import time
import random
import json
from bs4 import BeautifulSoup
from datetime import datetime
from .modules.classes import Filter_Jobs, Read_List_Of_Companies, Remove_Not_Found
from .modules import headers as h
# import modules.headers as h
# import modules.classes as c


FILE_PATH = "./data/params/bamboohr.txt"


def get_results(item: str, param: str):
    soup = BeautifulSoup(item, "lxml")
    logo = soup.find("img")["src"] if soup.find("img") else None
    results = soup.find(attrs={"type": "json"}).string
    data = json.loads(results)
    company = soup.find("div", class_="col-xs-12 col-sm-8 ResAts__header").find("img")["alt"] if soup.find(
        "div", class_="col-xs-12 col-sm-8 ResAts__header").find("img") else soup.find("div", class_="col-xs-12 col-sm-8 ResAts__header").find("h1").text
    for d in data:
        date = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
        post_date = datetime.timestamp(
            datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S"))
        apply_url = f"https://{param}.bamboohr.com/jobs/view.php?id={d['id']}"
        company_name = company.strip()
        position = d["jobOpeningName"].strip()
        location = f"{d['location']['city'].strip()}, {d['location']['state'].strip() if d['location']['state'] else d['location']['country'].strip()}"
        Filter_Jobs({
            "timestamp": post_date,
            "title": position,
            "company": company_name,
            "company_logo": logo,
            "url": apply_url,
            "location": location,
            "source": company_name,
            "source_url": f"https://{param}.bamboohr.com/jobs/"
        })


def get_url(companies: list):
    page = 1
    for company in companies:
        try:
            headers = {"User-Agent": random.choice(h.headers)}
            url = f"https://{company}.bamboohr.com/jobs/"
            response = requests.get(url, headers=headers)
            if response.ok:
                get_results(response.text, company)
                if page % 20 == 0:
                    time.sleep(5)
                page += 1
            elif response.status_code == 404:
                Remove_Not_Found(FILE_PATH, company)
        except:
            if response.status_code == 429:
                print(
                    f"=> bamboohr: Failed to scrape {company}. Status code: {response.status_code}")
                break
            else:
                print(
                    f"=> bamboohr: Failed to scrape {company}. Status code: {response.status_code}")


def main():
    companies = Read_List_Of_Companies(FILE_PATH)
    get_url(companies)


# main()
# sys.exit(0)
