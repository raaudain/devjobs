from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests, sys, json, time, re, random
from .modules import headers as h
from .modules import create_temp_json
# import modules.headers as h
# import modules.create_temp_json as create_temp_json

f = open(f"./data/params/us_and_ca.txt", "r")
locations = [location.strip() for location in f]
f.close()

m = open(f"./data/params/miami.txt", "r")
miamis = [miami.strip() for miami in m]
m.close()

scraped = create_temp_json.scraped
data = create_temp_json.data




def getJobs(item, location):
    for job in item:
        date = job.find("time", {"class": "result-date"})["datetime"]
        title = job.find("a", {"class": "result-title hdrlnk"}).text
        url = job.find("a", href=True)["href"]
        # location = re.search(r"https://(.*?).craigslist.org", url).group(1)
        location = location.strip()

        age = datetime.timestamp(datetime.now() - timedelta(days=14))
        postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d %H:%M"))

        if url not in scraped and age <= postDate:
            data.append({
                "timestamp": postDate,
                "title": title,
                "company": None,
                "url": url,
                "location": location,
                "source": "Craigslist",
                "source_url": "https://www.craigslist.org",
                "category": "job"
            })
            scraped.add(url)
            print(f"=> craigslist_jobs: Added {title} for {location}")
        else:
            print(f"=> craigslist_jobs: Already scraped or too old: {title} for {location}")
        


def getResults(item):
    soup = BeautifulSoup(item, "lxml")
    place = soup.find("title").text.replace(" technical support jobs - craigslist", "").replace(" software/qa/dba/etc jobs - craigslist", "").split(" ")
    location = ""

    for i in place:
        if len(place) > 1:
            if len(i) > 2:
                location += i.replace("/", "").capitalize()+" "
            else:
                location += i+" "
        else:
            location = i.capitalize()

    results = soup.find_all("div", {"class": "result-info"})

    # print(location, place)
    getJobs(results, location)

def getURL(items):
    count = 1

    for location in items:
        try:
            headers = {"User-Agent": random.choice(h.headers)}
            url = f"https://{location}.craigslist.org/search/sof?lang=en"
            response = requests.get(url, headers=headers)

            if response.ok:
                getResults(response.text)
            else:
                print(f"Error: {response.status_code}")

            if count % 10 == 0:
                time.sleep(5)
            
            count += 1
        except:
            print("=> craigslist_jobs: Continue to next")
            continue

def getURLMiami(items):
    count = 1

    for location in items:
        try:
            headers = {"User-Agent": random.choice(h.headers)}
            url = f"{location}d/software-qa-dba-etc/search/mdc/sof?lang=en"
            response = requests.get(url, headers=headers)

            if response.ok:
                getResults(response.text)
            else:
                print(f"Error: {response.status_code}")

            if count % 10 == 0:
                time.sleep(5)
            
            count += 1
        except:
            print("=> craigslist_jobs: Scrape failed. Going to next.")
            continue

def getURL_IT(items):
    count = 1

    for location in items:
        try:
            headers = {"User-Agent": random.choice(h.headers)}
            url = f"https://{location}.craigslist.org/search/tch?lang=en"
            response = requests.get(url, headers=headers)

            if response.ok:
                getResults(response.text)
            else:
                print(f"Error: {response.status_code}")

            if count % 10 == 0:
                time.sleep(5)
            
            count += 1
        except:
            print("=> craigslist_jobs: Continue to next")
            continue

def getURLMiami_IT(items):
    count = 1

    for location in items:
        try:
            headers = {"User-Agent": random.choice(h.headers)}
            url = f"{location}d/technical-support/search/mdc/tch?lang=en"
            response = requests.get(url, headers=headers)

            if response.ok:
                getResults(response.text)
            else:
                print(f"Error: {response.status_code}")

            if count % 10 == 0:
                time.sleep(5)
            
            count += 1
        except:
            print("=> craigslist_jobs: Scrape failed. Going to next.")
            continue

def main():
    getURL(locations)
    getURLMiami(miamis)
    getURL_IT(locations)
    getURLMiami_IT(miamis)
    # createJSON(data)

# main()

# sys.exit(0)