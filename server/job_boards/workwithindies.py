import requests
import sys
import random
from bs4 import BeautifulSoup
from datetime import datetime
from .modules.classes import Filter_Jobs
from .modules import headers as h


def get_results(item: str):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all("a", class_="job-card w-inline-block")
    for job in results:
        date = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
        post_date = datetime.timestamp(
            datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S"))
        position = job.find("div", class_="job-card-title").text
        company_name = job.find_all(
            "div", class_="job-card-text bold")[0].text
        logo = job.find("img", class_="company-logo")["src"] if job.find(
            "img", class_="company-logo", src=True) else None
        apply_url = "https://www.workwithindies.com"+job["href"]
        location = job.find_all("div", class_="job-card-text bold")[1].text
        Filter_Jobs({
            "timestamp": post_date,
            "title": position,
            "company": company_name,
            "company_logo": logo,
            "url": apply_url,
            "location": location,
            "source": "Work With Indies",
            "source_url": "https://www.workwithindies.com/"
        })


def get_url():
    headers = {"User-Agent": random.choice(h.headers)}
    url = "https://www.workwithindies.com/?categories=business%7Cprogramming%7Cqa-cs"
    response = requests.get(url, headers=headers)
    if response.ok:
        get_results(response.text)
    else:
        print("=> workwithindies: Error - Response status", response.status_code)


def main():
    get_url()


# main()
# sys.exit(0)
