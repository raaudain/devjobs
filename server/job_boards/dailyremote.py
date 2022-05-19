from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests
import sys
import re
import time
import random
from .modules.classes import Create_JSON, Filter_Jobs
from .modules import headers as h
from .modules import create_temp_json
# import modules.create_temp_json as create_temp_json
# import modules.headers as h


def get_results(item):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all("article")
    scraped = Create_JSON.scraped
    for job in results:
        date = job.find(
            class_="company-name display-flex").find_all("span")[4].text.strip()
        title = job.find(class_="job-position").text.strip()
        company = job.find(
            class_="company-name display-flex").find_all("span")[0].text.strip()
        link = job.find("a", class_="primary-btn apply-link",
                        href=True)["href"].strip()
        url = "https://dailyremote.com"+link if "apply" in link else link
        logo = "https://dailyremote.com" + \
            job.find(class_="pic")["src"] if job.find(class_="pic") else None
        location = job.find_all("span", class_="meta-holder")[0].text.strip()
        if "a second ago" in date:
            time = datetime.now() - timedelta(seconds=1)
            date = datetime.strftime(time, "%Y-%m-%d %H:%M:%S")
        elif "seconds" in date or "second" in date:
            seconds = re.sub("[^0-9]", "", date)
            time = datetime.now() - timedelta(seconds=int(seconds))
            date = datetime.strftime(time, "%Y-%m-%d %H:%M:%S")
        elif "a minute ago" in date:
            time = datetime.now() - timedelta(minutes=1)
            date = datetime.strftime(time, "%Y-%m-%d %H:%M:%S")
        elif "minutes" in date or "minute" in date:
            minutes = re.sub("[^0-9]", "", date)
            time = datetime.now() - timedelta(minutes=int(minutes))
            date = datetime.strftime(time, "%Y-%m-%d %H:%M:%S")
        elif "an hour ago" in date:
            time = datetime.now() - timedelta(hours=1)
            date = datetime.strftime(time, "%Y-%m-%d %H:%M:%S")
        elif "hours" in date or "hour" in date:
            hours = re.sub("[^0-9]", "", date)
            time = datetime.now() - timedelta(hours=int(hours))
            date = datetime.strftime(time, "%Y-%m-%d %H:%M:%S")
        elif "yesterday" in date:
            time = datetime.now() - timedelta(days=1)
            date = datetime.strftime(time, "%Y-%m-%d %H:%M:%S")
        elif re.match("[0-9]", date):
            day = re.sub("[^0-9]", "", date)
            time = datetime.now() - timedelta(days=int(day))
            date = datetime.strftime(time, "%Y-%m-%d %H:%M:%S")
        elif "today" in date:
            time = datetime.now()
            date = datetime.strftime(time, "%Y-%m-%d %H:%M:%S")
        age = datetime.timestamp(datetime.now() - timedelta(days=30))
        post_date = datetime.timestamp(
            datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))
        if company not in scraped:
            Filter_Jobs({
                "timestamp": post_date,
                "title": title,
                "company": company,
                "company_logo": logo,
                "url": url,
                "location": location,
                "source": "Daily Remote",
                "source_url": "https://dailyremote.com",
                "category": "job"
            })


def get_url():
    page = 1
    while page <= 500:
        print(f"=> dailyremote: Scraping page {page}")
        try:
            headers = {"User-Agent": random.choice(h.headers)}
            url = f"https://dailyremote.com/remote-software-development-jobs?search=&page={page}&sort_by=time#main"
            response = requests.get(url, headers=headers).text
            get_results(response)
            time.sleep(0.05)
            page += 1
        except:
            print(f"=> dailyremote: Error on page {page}")
            break


def main():
    get_url()


# main()
# sys.exit(0)
