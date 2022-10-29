import requests
import sys
import time
import random
from bs4 import BeautifulSoup
from datetime import datetime
from .helpers.classes import FilterJobs, ReadListOfCompanies, UpdateKeyValues
from .helpers import headers as h
# import modules.classes as c
# import modules.create_temp_json as create_temp_json
# import modules.headers as h


FILE_PATH = "./data/params/key_values.txt"


def get_results(item: str, url: str):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all("div", class_="open-position-item-contents")
    logo = soup.find(class_="hero-logo")["style"].replace("background: url(", "").replace(
        ") no-repeat center center; background-size: contain;", "") if soup.find(class_="hero-logo") else None
    for job in results:
        date = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
        post_date = datetime.timestamp(
            datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))
        title = job.find("p", class_="open-position--job-title").text
        company = job.find("a")["data-company"]
        apply_url = job.find("a", href=True)["href"]
        location = job.find(
            "div", class_="open-position--job-information").find_all("p")[0].text
        FilterJobs({
            "timestamp": post_date,
            "title": title,
            "company": company,
            "company_logo": logo,
            "url": apply_url,
            "location": location,
            "source": "Key Values",
            "source_url": url,
        })


def get_url(params: list):
    for param in params:
        headers = {"User-Agent": random.choice(h.headers)}
        url = f"https://www.keyvalues.com{param}"
        response = requests.get(url, headers=headers)
        if response.ok:
            get_results(response.text, url)
        else:
            print(f"=> key_values: Error. Status code:", response.status_code)
        time.sleep(2)


def main():
    UpdateKeyValues.filter_companies()
    params = ReadListOfCompanies(FILE_PATH)
    get_url(params)


# main()
# sys.exit(0)
