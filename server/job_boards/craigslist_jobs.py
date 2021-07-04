from bs4 import BeautifulSoup
from datetime import datetime, timedelta
# from ..functions.create_temp_json import tempJSON
import requests, sys, json, time, re
# import modules.create_temp_json as create_temp_json
from .modules import create_temp_json
# from requests.adapters import HTTPAdapter
# from requests.packages.urllib3.util.retry import Retry


f = open(f"./data/params/us_and_ca.txt", "r")
locations = [location.rstrip() for location in f]
f.close()

m = open(f"./data/params/miami.txt", "r")
miamis = [miami.rstrip() for miami in m]
m.close()

scraped = create_temp_json.scraped
data = create_temp_json.data

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}


def getJobs(item, place):
    for job in item:
        date = job.find("time", {"class": "result-date"})["datetime"]
        title = job.find("a", {"class": "result-title hdrlnk"}).text
        url = job.find("a", href=True)["href"]
        location = re.search(r"https://(.*?).craigslist.org", url).group(1)

        age = datetime.timestamp(datetime.now() - timedelta(days=7))
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
            print(f"=> craigslist_jobs: Added {title} for {place}")
        else:
            print(f"=> craigslist_jobs: Already scraped {title} for {place}")
        


def getResults(item, place):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all("div", {"class": "result-info"})
    getJobs(results, place)

def getURL(items):
    # session = requests.Session()
    # retry = Retry(connect=3, backoff_factor=2)
    # adapter = HTTPAdapter(max_retries=retry)
    # session.mount('http://', adapter)
    # session.mount('https://', adapter)
    
    for location in items:
        try:
            url = f"https://{location}.craigslist.org/search/sof?lang=en"
            response = requests.get(url, headers=headers).text
            getResults(response, location)
        except:
            print("=> craigslist_jobs: Continue to next")
            continue

def getURLMiami(items):
    # session = requests.Session()
    # retry = Retry(connect=3, backoff_factor=1)
    # adapter = HTTPAdapter(max_retries=retry)
    # session.mount("http://", adapter)
    # session.mount("https://", adapter)

    for location in items:
        try:
            url = f"{location}d/software-qa-dba-etc/search/mdc/sof?lang=en"
            response = requests.get(url, headers=headers).text
            getResults(response, location)
        except:
            print("=> craigslist_jobs: Scrape failed. Going to next.")
            pass

def main():
    getURL(locations)
    getURLMiami(miamis)
    # createJSON(data)

# main()

# sys.exit(0)