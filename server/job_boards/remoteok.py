from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json, requests, sys, random
from .modules import create_temp_json
from .modules import headers as h


def get_jobs(item: list):
    data = create_temp_json.data
    scraped = create_temp_json.scraped

    for job in item:
        date =  job.find("time")["datetime"].replace("T", " ")[:-9] if job.find("time") else None
        title = job.find("h2", {"itemprop": "title"}).text if job.find("h2", {"itemprop": "title"}) else None
        company = job.find("h3", {"itemprop": "name"}).text if job.find("h3", {"itemprop": "name"}) else None
        url = "https://remoteok.io"+job.find("a", class_="preventLink", href=True)["href"] if job.find("a", class_="preventLink", href=True) else None
        location = job.find("div", class_="location tooltip").text.strip() if job.find("div", class_="location tooltip") else "Remote"

        if company not in scraped:
            # if date: date = job.find("time")["datetime"].replace("T", " ")[:-9]
            # if title: title = job.find("h2", {"itemprop": "title"}).text
            # if company: company = job.find("h3", {"itemprop": "name"}).text
            # if url: url = "https://remoteok.io"+job.find("a", {"class": "preventLink"}, href=True)["href"]

            # if location:
            #     location = job.find("div", {"class": "location tooltip"}).text.strip()
            # else:
            #     location = "Remote"

            age = datetime.timestamp(datetime.now() - timedelta(days=30))
            postDate = datetime.timestamp(datetime.strptime(str(date), "%Y-%m-%d %H:%M"))
            
            if age <= postDate:
                data.append({
                    "timestamp": postDate,
                    "title": title,
                    "company": company,
                    "url": url,
                    "location": location,
                    "source": "Remote OK",
                    "source_url": "https://remoteok.io/",
                    "category": "job"
                })
                print(f"=> remoteok: Added {title} for {company}")


def get_results(item: str):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all("tr")
    get_jobs(results)


def get_url():
    headers = {"User-Agent": random.choice(h.headers)}
    url = f"https://remoteok.io/remote-dev-jobs"
    response = requests.get(url, headers=headers)

    if response.ok: get_results(response.text)
    else: print("=> remoteok: Error - Response status", response.status_code)


def main():
    get_url()
