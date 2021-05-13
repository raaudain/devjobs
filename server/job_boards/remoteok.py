from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json, requests, sys
from .modules import create_temp_json


data = create_temp_json.data


def getJobs(item):
    for job in item:
        date = job.find("time")
        title = job.find("h2", {"itemprop": "title"})
        company = job.find("h3", {"itemprop": "name"})
        url = job.find("a", {"class": "preventLink"}, href=True)
        region = job.find("div", {"class": "location tooltip"})

        if date:
            date = job.find("time")["datetime"].replace("T", " ")[:-9]
        
        if title:
            title = job.find("h2", {"itemprop": "title"}).text

        if company:
            company = job.find("h3", {"itemprop": "name"}).text

        if url:
            url = "https://remoteok.io"+job.find("a", {"class": "preventLink"}, href=True)["href"]

        if region:
            region = job.find("div", {"class": "location tooltip"}).text.lstrip()
        else:
            region = "Remote"

        if title:
            title = job.find("h2", {"itemprop": "title"}).text

            age = datetime.timestamp(datetime.now() - timedelta(days=7))
            postDate = datetime.timestamp(datetime.strptime(str(date), "%Y-%m-%d %H:%M"))
            
            if age <= postDate:
                data.append({
                    "timestamp": postDate,
                    "title": title,
                    "company": company,
                    "url": url,
                    "region": region,
                    "category": "job"
                })
                print(f"=> remoteok: Added {title}")

def getResults(item):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all("tr")
    getJobs(results)

def getURL():
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}

    url = f"https://remoteok.io/remote-dev-jobs"
    response = requests.get(url, headers=headers).text
    getResults(response)

def main():
    getURL()
