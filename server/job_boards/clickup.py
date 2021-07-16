from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests, sys
from .modules import create_temp_json
# import modules.create_temp_json as create_temp_json


data = create_temp_json.data

def getJobs(item):
    date = datetime.strftime(datetime.now(), "%Y-%m-%d")
    title = item.text
    company = "ClickUp"
    url = "https://clickup.com"+item["href"]
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
    results = soup.find_all("a", {"class": "current-vacancies__jobs_description"})

    for i in results:
        if "Engineer" in i.text or "Tech" in i.text or "Support" in i.text or "IT " in i.text:
            getJobs(i)

    # getJobs(results)
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