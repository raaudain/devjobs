from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from .modules import create_temp_json
# from .modules.headers import headers as h
# import modules.create_temp_json as create_temp_json
# import modules.headers as h
import requests, sys, random


def get_jobs(item: list):
    data = create_temp_json.data
    scraped = create_temp_json.scraped

    for job in item:
        try:
            date = job.find("time")["datetime"].replace("T", " ").replace("Z", "") if job.find("time") else datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
            title = job.find("span", class_="title").text.strip()
            company = job.find("span", class_="company").text.strip()
            url = "https://www.weworkremotely.com"+job.find_all("a", href=True)[1]["href"]
            location = job.find("span", class_="region company").contents[0] if job.find("span", class_="region company") else "Remote"
            logo = None
            
            # if location:
            #     location = job.find("span", {"class": "region company"}).contents[0]
            # else:
            #     location = "Remote"

            # if date:
            #     date = job.find("time")["datetime"].replace("T", " ").replace("Z", "")[:-3]
            # else:
            #     date = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M")

            age = datetime.timestamp(datetime.now() - timedelta(days=30))
            postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))

            if age <= postDate and company not in scraped:
                data.append({
                    "timestamp": postDate,
                    "title": title,
                    "company": company,
                    "company_logo": logo,
                    "url": url,
                    "location": location,
                    "source": "WeWorkRemotely",
                    "source_url": "https://weworkremotely.com/",
                    "category": "job"
                })
            print(f"=> weworkremotely: Added {title}")
        except:
            pass


def get_results(item: str):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all("li", class_=["feature",""])
    get_jobs(results)


def get_url():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"}
    url = f"https://weworkremotely.com/remote-jobs/search?term=&button=&categories%5B%5D=2&categories%5B%5D=17&categories%5B%5D=18&categories%5B%5D=6"
    response = requests.get(url, headers=headers)

    if response.ok: get_results(response.text)
    else: print("=> weworkremotely: Error - Response status", response.status_code)


def main():
    get_url()


main()
sys.exit(0)