import requests
import sys
import time
import random
from bs4 import BeautifulSoup
from datetime import datetime
from .modules.classes import Filter_Jobs, Read_List_Of_Companies, Remove_Not_Found
from .modules import create_temp_json
from .modules import headers as h
# import modules.create_temp_json as create_temp_json
# import modules.headers as h
# import modules.classes as c


FILE_PATH = "./data/params/lever_co.txt"


def get_results(item: str, name: str):
    soup = BeautifulSoup(item, "lxml")
    logo = soup.find(class_="main-header-logo").find("img")[
        "src"] if soup.find(class_="main-header-logo") else None
    results = soup.find_all("a", class_="posting-title")
    company = soup.find("title").text.strip()
    source_url = f"https://jobs.lever.co/{name}"
    for job in results:
        date = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
        post_date = datetime.timestamp(
            datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))
        title = job.find("h5", {"data-qa": "posting-name"}).text
        company_name = company
        apply_url = job["href"]
        location = job.find("span", class_="sort-by-location posting-category small-category-label").text if job.find(
            "span", class_="sort-by-location posting-category small-category-label") else None
        Filter_Jobs({
            "timestamp": post_date,
            "title": title,
            "company": company_name,
            "company_logo": logo,
            "url": apply_url,
            "location": location,
            "source": company_name,
            "source_url": source_url
        })


def get_url(companies: list):
    count = 1
    for name in companies:
        headers = {"User-Agent": random.choice(h.headers)}
        url = f"https://jobs.lever.co/{name}"
        response = requests.get(url, headers=headers)
        if response.ok:
            get_results(response.text, name)
        elif response.status_code == 404:
            Remove_Not_Found(FILE_PATH, name)
        else:
            print(
                f"=> lever.co: Error for {name} - Response status", response.status_code)
        if count % 20 == 0:
            time.sleep(5)
        count += 1


def main():
    companies = Read_List_Of_Companies(FILE_PATH)
    get_url(companies)


# main()
# sys.exit(0)
