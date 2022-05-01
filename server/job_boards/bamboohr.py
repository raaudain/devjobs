import requests
import sys
import time
import random
import json
from bs4 import BeautifulSoup
from datetime import datetime
from .modules.classes import Create_Temp_JSON, List_Of_Companies, Page_Not_Found
from .modules import create_temp_json
from .modules import headers as h
# import modules.create_temp_json as create_temp_json
# import modules.headers as h
# import modules.classes as c


FILE_PATH = "./data/params/bamboohr.txt"


def get_jobs(date: str, url: str, company: str, position: str, location: str, logo: str, param: str):
    data = create_temp_json.data
    scraped = create_temp_json.scraped
    post_date = datetime.timestamp(
        datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S"))
    data.append({
        "timestamp": post_date,
        "title": position,
        "company": company,
        "company_logo": logo,
        "url": url,
        "location": location,
        "source": company,
        "source_url": f"https://{param}.bamboohr.com/jobs/",
        "category": "job"
    })
    scraped.add(company)
    print(f"=> bamboohr: Added {position} for {company}")


def get_results(item: str, param: str):
    try:
        soup = BeautifulSoup(item, "lxml")
        logo = soup.find("img")["src"] if soup.find("img") else None
        results = soup.find(attrs={"type": "json"}).string
        data = json.loads(results)
        company = soup.find("div", class_="col-xs-12 col-sm-8 ResAts__header").find("img")["alt"] if soup.find(
            "div", class_="col-xs-12 col-sm-8 ResAts__header").find("img") else soup.find("div", class_="col-xs-12 col-sm-8 ResAts__header").find("h1").text
        for d in data:
            if "Engineer" in d["jobOpeningName"] or "Data" in d["jobOpeningName"] or "IT " in d["jobOpeningName"] or "Tech" in d["jobOpeningName"] or "Support" in d["jobOpeningName"] or "Cloud" in d["jobOpeningName"] or "Software" in d["jobOpeningName"] or "Developer" in d["jobOpeningName"] and ("Electrical" not in d["jobOpeningName"] and "HVAC" not in d["jobOpeningName"] and "Mechnical" not in d["jobOpeningName"]):
                date = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
                apply_url = f"https://{param}.bamboohr.com/jobs/view.php?id={d['id']}"
                company_name = company.strip()
                position = d["jobOpeningName"].strip()
                locations_string = f"{d['location']['city'].strip()}, {d['location']['state'].strip() if d['location']['state'] else d['location']['country'].strip()}"
                get_jobs(date, apply_url, company_name,
                         position, locations_string, logo, param)
    except AttributeError as err:
        print(f"=> bamboohr: Error for {param}.", err)


def get_url(companies: list):
    page = 1
    for company in companies:
        headers = {"User-Agent": random.choice(h.headers)}
        url = f"https://{company}.bamboohr.com/jobs/"
        response = requests.get(url, headers=headers)
        if response.ok:
            get_results(response.text, company)
            if page % 10 == 0:
                time.sleep(5)
            page += 1
        elif response.status_code == 404:
            not_found = Page_Not_Found(FILE_PATH, company)
            not_found.remove_unwanted()
        elif response.status_code == 429:
            print(
                f"=> bamboohr: Failed to scrape {company}. Status code: {response.status_code}")
            break
        else:
            print(
                f"=> bamboohr: Failed to scrape {company}. Status code: {response.status_code}")


def main():
    companies = List_Of_Companies(FILE_PATH).read_file()
    random.shuffle(companies)
    get_url(companies)


# main()
# sys.exit(0)
