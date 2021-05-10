from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json, requests, sys, re
import modules.create_temp_json as create_temp_json


data = create_temp_json.data
exclude = set()
exclude.add("month")
exclude.add("months")

# t = open(f"./data/temp/temp_data.json", "r+")
# t.truncate(0)
# t.close()


def createJSON(item):
    with open("./data/temp/temp_data.json", "a", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def getJobs(item):
    # print(item)
    for job in item:
        date = job.find("date").text
        title = job.find("span", {"class": "font-weight-bold larger"}).text
        company = "".join(job.find("p", {"class": "m-0 text-secondary"}).text.split("|")[0]).strip()
        url = "https://remote.co"+job["href"]
        region = "Remote"

        if "hours" in date or "hour" in date:
            hours = re.sub("[^0-9]", "", date)
            time = datetime.now() - timedelta(hours=int(hours))
            date = datetime.strftime(time, "%Y-%m-%d %H:%M")
        elif "days" in date or "day" in date:
            day = re.sub("[^0-9]", "", date)
            time = datetime.now() - timedelta(days=int(day))
            date = datetime.strftime(time, "%Y-%m-%d %H:%M")
        elif "week" in date:
            time = datetime.now() - timedelta(days=7)
            date = datetime.strftime(time, "%Y-%m-%d %H:%M")
        else:
            continue

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
        print(f"=> remote.co: Added {title}")

def getResults(item):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all("a", {"class": "card m-0 border-left-0 border-right-0 border-top-0 border-bottom"})
    getJobs(results)

def getURL():
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}
    url = f"https://remote.co/remote-jobs/developer"
    response = requests.get(url, headers=headers).text
    getResults(response)

def main():
    getURL()
    # createJSON(data)

# main()

# sys.exit(0)