from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests, sys
from .modules import create_temp_json
# import modules.create_temp_json as create_temp_json


data = create_temp_json.data

def getJobs(item):
    for job in item:
        date = datetime.strftime(datetime.now(), "%Y-%m-%d")
        title = job.find("div", {"class": "job-card-title"}).text
        company = job.find_all("div", {"class": "job-card-text bold"})[0].text
        url = "https://www.workwithindies.com"+job["href"]
        location = job.find_all("div", {"class": "job-card-text bold"})[1].text

        # print(date, title, company, url, location)
        postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d"))

        data.append({
            "timestamp": postDate,
            "title": title,
            "company": company,
            "url": url,
            "location": location,
            "source": "Work With Indies",
            "source_url": "https://www.workwithindies.com/",
            "category": "job"
        })
        print(f"=> workwithindies: Added {title}")

def getResults(item):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all("a", {"class": "job-card w-inline-block"})
    getJobs(results)
    # print(results)

def getURL():
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}

    url = f"https://www.workwithindies.com/?categories=programming"
    response = requests.get(url, headers=headers)

    if response.ok:
        getResults(response.text)
    else:
        print("=> workwithindies: Error - Response status", response.status_code)
    # print(response)

def main():
    getURL()

# main()
# sys.exit(0)