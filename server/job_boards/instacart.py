from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests
from .modules import create_temp_json
# import modules.create_temp_json as create_temp_json


data = create_temp_json.data

def getJobs(item):

    for job in item:
        date = datetime.strftime(datetime.now(), "%Y-%m-%d")
        title = job.find("a").text
        company = "Instacart"
        url = job.find("a", href=True)["href"]
        location = job.find_all("span")[1].text

        postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d"))

        # print(date, title, company, url, location)

        data.append({
            "timestamp": postDate,
            "title": title,
            "company": company,
            "url": url,
            "location": location,
            "source": company,
            "source_url": "https://www.instacart.com/",
            "category": "job"
        })
        print(f"=> instacart: Added {title}")

def getResults(item):
    teams = ("team-19", "team-13", "team-23", "team-26", "team-38", "team-40", "team-42", "team-43")

    soup = BeautifulSoup(item, "lxml")
    unfilteredResults = soup.find_all("div", {"class": "card"})
    results = []

    for result in unfilteredResults:
        if result.div["id"] in teams:
            results.extend(result.find_all("div", {"class" : "jobs-section"}))
    # print("======================>>>>>>>>>>>>>", results)
    getJobs(results)

def getURL():
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}

    url = f"https://instacart.careers/current-openings/"
    response = requests.get(url, headers=headers).text
    getResults(response)
    # print(response)

def main():
    getURL()

# main()