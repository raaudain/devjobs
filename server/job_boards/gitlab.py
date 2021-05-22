from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests, sys
from .modules import create_temp_json
# import modules.create_temp_json as create_temp_json


data = create_temp_json.data

def getJobs(item):
    for job in item:
        date = datetime.strftime(datetime.now(), "%Y-%m-%d")
        title = job.find("a", href=True).text
        company = "GitLab"
        url = "https://boards.greenhouse.io"+job.find("a", href=True)["href"]
        location = job.find("span", {"class": "location"}).text

        # print(date, title, company, url, location)
        postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d"))

        data.append({
            "timestamp": postDate,
            "title": title,
            "company": company,
            "url": url,
            "location": location,
            "source": "GitLab",
            "source_url": "https://www.gitlab.com/",
            "category": "job"
        })
        print(f"=> gitlab: Added {title}")

def getResults(item):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all("section", {"class": "level-0"})

    for result in results:
        if result.find("h3").text == "Engineering":
            results = result.find_all("div", {"class": "opening"})


    getJobs(results)
    # print(results)

def getURL():
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}

    url = f"https://boards.greenhouse.io/gitlab"
    response = requests.get(url, headers=headers).text
    getResults(response)
    # print(response)

def main():
    getURL()

# main()
# sys.exit(0)