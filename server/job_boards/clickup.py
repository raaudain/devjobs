from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests, sys
from .modules import create_temp_json
# import modules.create_temp_json as create_temp_json


data = create_temp_json.data

def getJobs(item):
    for job in item:
        date = datetime.strftime(datetime.now(), "%Y-%m-%d")
        title = job.text
        company = "ClickUp"
        url = "https://clickup.com"+job["href"]
        location = "See description"

        # print(date, title, company, url, location)
        postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d"))

        data.append({
            "timestamp": postDate,
            "title": title,
            "company": company,
            "url": url,
            "location": location,
            "source": "ClickUp",
            "source_url": "https://clickup.com",
            "category": "job"
        })
        print(f"=> clickup: Added {title}")

def getResults(item):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find("div", {"class": "current-vacancies__item current-vacancies__item_yellow"}).find_all("a", {"class": "current-vacancies__jobs_description"})

    getJobs(results)
    # print(results)

def getURL():
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0"}

    url = f"https://clickup.com/careers"
    response = requests.get(url, headers=headers).text
    getResults(response)
    # print(response)

def main():
    getURL()

# main()
# sys.exit(0)