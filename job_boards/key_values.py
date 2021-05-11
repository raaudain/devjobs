from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json, requests, sys
import modules.create_temp_json as create_temp_json
import modules.update_key_values as updateKeyValues

f = open(f"./data/params/key_values.txt", "r")
params = [param.rstrip() for param in f]
f.close()

data = create_temp_json.data
exclude = set()
exclude.add("See All Open Jobs")
exclude.add("See All Open Roles")
exclude.add("Interested in joining?")
exclude.add("All Jobs at CareGuide")
exclude.add("See All Job Openings")
exclude.add("See All Open Positions")
exclude.add("")

def getJobs(item):
    for job in item:
        date = datetime.strftime(datetime.now(), "%Y-%m-%d")
        title = job.find("p", {"class": "open-position--job-title"}).text
        company = job.find("a")["data-company"]
        url = job.find("a", href=True)["href"]
        region = job.find("div", {"class": "open-position--job-information"}).find_all("p")[0].text

        postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d"))

        if title not in exclude:
            data.append({
                "timestamp": postDate,
                "title": title,
                "company": company,
                "url": url,
                "region": region,
                "category": "job"
            })
            print(f"=> key_values: Added {title}")

def getResults(item):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all("div", {"class": "open-position-item-contents"})
    getJobs(results)

def getURL():
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}

    for param in params:
        url = f"https://www.keyvalues.com{param}"
        response = requests.get(url, headers=headers).text
        getResults(response)

def main():
    updateKeyValues.main()
    getURL()

main()