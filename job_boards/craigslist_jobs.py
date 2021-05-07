from bs4 import BeautifulSoup
from datetime import datetime, timedelta
# from ..functions.create_temp_json import tempJSON
import requests, sys, json
# sys.path.insert(0, "./functions/create_temp_json.py")

# from create_temp_json.py import data

# print(tempJSON.data)


f = open(f"./data/craigslist/us_and_ca.txt", "r")
locations = [location.rstrip() for location in f]
f.close()

m = open(f"./data/craigslist/miami.txt", "r")
miamis = [miami.rstrip() for miami in m]
m.close()

t = open(f"./data/temp/temp_data.json", "r+")
t.truncate(0)
t.close()

scraped = set()
data = []

def createJSON(item):
    with open("./data/temp/temp_data.json", "a", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def getJobs(item):
    for job in item:
        date = job.find("time", {"class": "result-date"})["datetime"]
        title = job.find("a", {"class": "result-title hdrlnk"}).text
        url = job.find("a", href=True)["href"]
        region = str(job.find("span", {"class": "result-hood"})).replace('<span class="result-hood"> (', "").replace(")</span>", "")
        
        age = datetime.timestamp(datetime.now() - timedelta(days=7))
        postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d %H:%M"))

        if age <= postDate and url not in scraped:
            data.append({
                "timestamp": postDate,
                "title": title,
                "company": None,
                "url": url,
                "region": region,
                "category": "job"
            })
            print(f"craigslist_jobs: Added {title}")
        
        scraped.add(url)
        # print(scraped)

def getResults(item):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all("div", {"class": "result-info"})
    getJobs(results)

def getURL(items):
    for location in items:
        url = f"https://{location}.craigslist.org/search/sof?lang=en"
        response = requests.get(url).text
        getResults(response)

def getURLMiami(items):
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}

    for location in items:
        url = f"{location}d/software-qa-dba-etc/search/mdc/sof?lang=en"
        response = requests.get(url, headers=headers).text
        getResults(response)

def main():
    getURL(locations)
    getURLMiami(miamis)
    createJSON(data)

main()

sys.exit(0)