import requests
import sys
import time
import random
from bs4 import BeautifulSoup
from datetime import datetime
from .helpers import headers as h
from .helpers.classes import FilterJobs, ReadListOfCompanies, RemoveNotFound
# import modules.headers as h


FILE_PATH = "./data/params/jobvite.txt"


def get_results(item: str, name: str):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all(
        class_="jv-job-list") if soup.find_all(class_="jv-job-list") else None
    company = soup.find("title").text.replace("Careers", "").replace(
        "| Available job openings", "").replace("Job listings |", "").strip() if soup.find("title") else None
    logo = soup.find(class_="logo")["src"] if soup.find(
        class_="logo", src=True) else None
    if results and company:
        for r in results:
            title = r.find(class_="jv-job-list-name").text.strip() if r.find(
                class_="jv-job-list-name") else r.find("a").text.strip()
            date = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
            post_date = datetime.timestamp(
                datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S"))
            apply_url = "https://jobs.jobvite.com" + \
                r.find("a")["href"].strip()
            company_name = company
            position = title
            location = r.find("td", class_="jv-job-list-location").text.strip() if r.find(
                "td", class_="jv-job-list-location") else "See description for location"
            FilterJobs({
                "timestamp": post_date,
                "title": position,
                "company": company_name,
                "company_logo": logo,
                "url": apply_url,
                "location": location,
                "source": company_name,
                "source_url": f"https://jobs.jobvite.com/careers/{name}"
            })


def get_url(companies: list):
    count = 1
    for name in companies:
        headers = {"User-Agent": random.choice(h.headers)}
        url = f"https://jobs.jobvite.com/{name}/search"
        try:
            response = requests.get(url, headers=headers)
            if response.ok:
                get_results(response.text, name)
            elif response.status_code == 404:
                RemoveNotFound(FILE_PATH, name)
            else:
                res = requests.get(
                    f"https://jobs.jobvite.com/{name}/jobs", headers=headers)
                if res.ok:
                    get_results(res.text, name)
                else:
                    print(
                        f"=> jobvite: Scrape failed for {name}. Status code: {res.status_code}")
        except:
            print("=> jobvite: Connection error:", name)
        if count % 20 == 0:
            time.sleep(5)
        else:
            time.sleep(0.2)
        count += 1


def main():
    companies = ReadListOfCompanies(FILE_PATH)
    get_url(companies)


# main()
# sys.exit(0)
