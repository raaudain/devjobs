from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json, requests, sys
import modules.create_temp_json as create_temp_json


data = create_temp_json.data

# t = open(f"./data/temp/temp_data.json", "r+")
# t.truncate(0)
# t.close()

def createJSON(item):
    with open("./data/temp/temp_data.json", "a", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def getJobs(item):
    for job in item:
        date = datetime.strptime(job.find_all("small")[1].text+" "+str(datetime.today().year)
, "%b %d %Y")
        title = job.find("strong").text
        company = job.find("small").text
        url = "https://nocsok.com/"+job.find("a", href=True)["href"].replace("#", "")
        region = job.find("h5").text.lstrip().rstrip()

        age = datetime.timestamp(datetime.now() - timedelta(days=7))
        postDate = datetime.timestamp(datetime.strptime(str(date)[:-9], "%Y-%m-%d"))

        if age <= postDate:
            data.append({
                "timestamp": postDate,
                "title": title,
                "company": company,
                "url": url,
                "region": region,
                "category": "job"
            })
            print(f"nocsok: Added {title}")

def getResults(item):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all("div", {"class": "w-100 jobboard-card-child"})
    # print(results)
    getJobs(results)

def getURL():
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}

    url = f"https://nocsok.com/"
    response = requests.get(url, headers=headers).text
    getResults(response)
    # print(response)

def main():
    getURL()
    # createJSON(data)

# main()

# sys.exit(0)