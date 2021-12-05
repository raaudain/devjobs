from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests, sys, random
from .modules import create_temp_json
from .modules import headers as h
# import modules.create_temp_json as create_temp_json
# import modules.headers as h


def get_jobs(item: list):
    data = create_temp_json.data
    scraped = create_temp_json.scraped

    for job in item:
        if job.find("time") and job.find("h3", {"itemprop": "name"}).text.strip() not in scraped:
            date =  job.find("time")["datetime"].replace("T", " ")[:-6]
            title = job.find("h2", {"itemprop": "title"}).text.strip()
            company = job.find("h3", {"itemprop": "name"}).text.strip()
            logo = job.find(class_="logo lazy lazyloaded")["src"].replace(",quality=50", "") if job.find(class_="logo lazy lazyloaded", src=True) else None
            url = "https://remoteok.io"+job.find("a", class_="preventLink", href=True)["href"]
            location = job.find("div", class_="location tooltip").text.strip() if job.find("div", class_="location tooltip") else "Remote"

            age = datetime.timestamp(datetime.now() - timedelta(days=30))
            postDate = datetime.timestamp(datetime.strptime(str(date), "%Y-%m-%d %H:%M%S"))
            
            if age <= postDate:
                data.append({
                    "timestamp": postDate,
                    "title": title,
                    "company": company,
                    "company_logo": logo,
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


# main()
# sys.exit(0)