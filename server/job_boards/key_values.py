from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json, requests, sys, time, random
# import modules.create_temp_json as create_temp_json
# import modules.update_key_values as updateKeyValues
# import modules.headers as h
from .modules import create_temp_json
from .modules import update_key_values
from .modules import headers as h


f = open(f"./data/params/key_values.txt", "r")
params = [param.rstrip() for param in f]
f.close()

data = create_temp_json.data
scraped = create_temp_json.scraped

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
        location = job.find("div", {"class": "open-position--job-information"}).find_all("p")[0].text

        postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d"))

        if title not in exclude and url not in scraped:
            data.append({
                "timestamp": postDate,
                "title": title,
                "company": company,
                "url": url,
                "location": location,
                "source": "Key Values",
                "source_url": "https://www.keyvalues.com",
                "category": "job"
            })
            scraped.add(url)
            print(f"=> key_values: Added {title} for {company}")
        else:
            print(f"=> key_values: Already scraped {title} for {company}")


def getResults(item):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all("div", {"class": "open-position-item-contents"})
    getJobs(results)

def getURL():

    for param in params:
        try:
            headers = {"User-Agent": random.choice(h.headers)}
            url = f"https://www.keyvalues.com{param}"
            response = requests.get(url, headers=headers).text
            getResults(response)
            time.sleep(5)
        except:
            print(f"=> key_values: Failed to scrape {param}")
            continue


def main():
    update_key_values.main()
    getURL()
