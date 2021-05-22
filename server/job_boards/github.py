from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests, sys
from .modules import create_temp_json
# import modules.create_temp_json as create_temp_json


data = create_temp_json.data

def getJobs(item):
    for job in item:
        date = datetime.strftime(datetime.now(), "%Y-%m-%d")
        title = job.find("span").text
        company = "GitHub"
        url = job["href"]
        location = job.find("span", {"class": "d-block float-md-right color-text-primary"}).text

        # print(date, title, company, url, location)
        postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d"))

        data.append({
            "timestamp": postDate,
            "title": title,
            "company": company,
            "url": url,
            "location": location,
            "source": "GitHub",
            "source_url": "https://www.github.com/",
            "category": "job"
        })
        print(f"=> github: Added {title}")

def getResults(item):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all("div", {"class": "Details js-details-container"})

    for result in results:
        if result.find("h3").text == "Engineering":
            results = result.find_all("a")


    getJobs(results)
    # print(results)

def getURL():
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}

    url = f"https://github.com/about/careers"
    response = requests.get(url, headers=headers).text
    getResults(response)
    # print(response)

def main():
    getURL()

# main()
# sys.exit(0)