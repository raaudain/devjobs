from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json, requests, sys


f = open(f"./data/craigslist/key_values.txt", "r")
params = [param.rstrip() for param in f]
f.close()

data = []

t = open(f"./data/temp/temp_data.json", "r+")
t.truncate(0)
t.close()

def createJSON(item):
    with open("./data/temp/temp_data.json", "a", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def getJobs(item):
    for job in item:
        date = datetime.strftime(datetime.now(), "%Y-%m-%d")
        title = job.find("p", {"class": "open-position--job-title"}).text
        company = job.find("a")["data-company"]
        url = job.find("a", href=True)["href"]
        region = job.find("div", {"class": "open-position--job-information"}).find_all("p")[0].text

        postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d"))

        # if title == "See All Open Jobs" or title == "See All Open Roles":
        #     print("Hello", title, company)

        if title not in "See All Open Jobs" or title not in "See All Open Roles":
            data.append({
                "timestamp": postDate,
                "title": title,
                "company": company,
                "url": url,
                "region": region,
                "category": "job"
            })
            print(f"key_values: Added {title}")

def getResults(item):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all("div", {"class": "open-position-item-contents"})
    # print(results)
    getJobs(results)

def getURL():
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}

    for param in params:
        url = f"https://www.keyvalues.com{param}"
        response = requests.get(url, headers=headers).text
        getResults(response)

def main():
    getURL()
    createJSON(data)

main()

sys.exit(0)