import requests
import sys
import time
import random
from datetime import datetime
from bs4 import BeautifulSoup
from .helpers.classes import FilterJobs, RemoveNotFound, ReadListOfCompanies
from .helpers import create_temp_json
from .helpers import headers as h
# import modules.create_temp_json as create_temp_json
# import modules.headers as h


FILE_PATH = "./data/params/jazzhr.txt"


def get_results(item: str, name: str):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all("li", class_="list-group-item")
    company = soup.find("meta", {"name": "twitter:title"})["content"].replace(
        " - Career Page", "") if soup.find("meta", {"name": "twitter:title"}) else None
    logo = soup.find(class_="").find("img")["src"] if soup.find(
        class_="").find("img", src=True) else None
    if results and company:
        for r in results:
            date = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
            post_date = datetime.timestamp(
                datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S"))
            apply_url = r.find("a")["href"].strip()
            company_name = company.strip()
            position = r.find("a").text.strip()
            location = r.find("ul").text.strip()
            FilterJobs({
                "timestamp": post_date,
                "title": position,
                "company": company_name,
                "company_logo": logo,
                "url": apply_url,
                "location": location,
                "source": company_name,
                "source_url": f"https://{name}.applytojob.com"
            })
    else:
        print(f"jazzhr => Error: check {company}")


def get_url(companies: list):
    page = 1
    for company in companies:
        try:
            headers = {"User-Agent": random.choice(h.headers)}
            url = f"https://{company}.applytojob.com"
            response = requests.get(url, headers=headers)
            if response.ok:
                get_results(response.text, company)
            elif response.status_code == 404:
                RemoveNotFound(FILE_PATH, company)
            else:
                f"=> jazzhr: Error for {company}. Status code: {response.status_code}"
            if page % 10 == 0:
                time.sleep(5)
            else:
                time.sleep(0.2)
            page += 1
        except Exception as e:
            print(f"=> jazzhr: Error for {company}. {e}")


def main():
    companies = ReadListOfCompanies(FILE_PATH)
    get_url(companies)


# main()
# sys.exit(0)
