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
        date = job.find("time")
        title = job.find("span", {"class": "title"}).text
        company = job.find("span", {"class": "company"}).text
        url = "https://www.weworkremotely.com"+job.find_all("a", href=True)[1]["href"]
        region = job.find("span", {"class": "region company"})
        
        if region:
            region = job.find("span", {"class": "region company"}).contents[0]
        else:
            region = None

        if date:
            date = job.find("time")["datetime"].replace("T", " ").replace("Z", "")[:-3]

        else:
            date = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M")

        age = datetime.timestamp(datetime.now() - timedelta(days=7))
        postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d %H:%M"))

        if age <= postDate:
            data.append({
                "timestamp": postDate,
                "title": title,
                "company": company,
                "url": url,
                "region": region,
                "category": "job"
            })
        print(f"weworkremotely: Added {title}")

def getResults(item):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find("div", {"class": "content"}).find_all("li", {"class": ["feature",""]})
    getJobs(results)

def getURL():
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}
    url = f"https://weworkremotely.com/remote-jobs/search?term=&button=&categories%5B%5D=2&categories%5B%5D=17&categories%5B%5D=18&categories%5B%5D=6"
    response = requests.get(url, headers=headers).text
    getResults(response)

def main():
    getURL()
    createJSON(data)

main()

sys.exit(0)