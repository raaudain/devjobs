from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json, requests, sys


data = []

t = open(f"./data/temp/temp_data.json", "r+")
t.truncate(0)
t.close()

def createJSON(item):
    with open("./data/temp/temp_data.json", "a", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def getJobs(item):
    for job in item:
        date = datetime.strptime(job.find("p", {"class": "text-lg font-bold text-teal-700"}).text, "%Y-%m-%d")
        title = job.find("h2", {"class": "text-xl leading-tight text-blue-900 capitalize md:-mt-1 xl:text-2xl"}).text
        company = job.find("p", {"class": "mb-1 text-sm text-blue-400"}).text
        url = "https://protege.dev"+job.find("a", href=True)["href"]
        region = None

        postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d"))
        print(date, time, company, ulr, region, postDate)
        data.append({
            "timestamp": postDate,
            "title": title,
            "company": company,
            "url": url,
            "region": region,
            "category": "job"
        })
        print(f"protege: Added {title}")

def getResults(item):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find("div", {"data-cy": "container"})
    print(results)
    # getJobs(results)

def getURL():
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}

    url = f"https://protege.dev"
    response = requests.get(url, headers=headers).text
    getResults(response)
    # print(response)

def main():
    getURL()
    createJSON(data)

main()

sys.exit(0)