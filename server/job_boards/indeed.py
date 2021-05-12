import modules.create_temp_json as create_temp_json
from bs4 import BeautifulSoup
import json, requests, sys
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


f = open(f"./data/params/zip_codes.txt", "r")
codes = [code.rstrip() for code in f]
f.close()

scraped = set()
data = create_temp_json.data

# t = open(f"./data/temp/temp_data.json", "r+")
# t.truncate(0)
# t.close()

def getJobs(item):
    for job in item:
        date = job.find("span", {"class": "date date-a11y"}).text.replace("\n", "")
        title = job.find("a", {"data-tn-element": "jobTitle"}).text.replace("\n", "")
        company = job.find("a", {"data-tn-element": "companyName"}).text.replace("\n", "")
        url = "https://www.indeed.com"+job.find("a", href=True)["href"]
        area = job.find("span", {"class": "location accessible-contrast-color-location"}).text
        
        # age = datetime.timestamp(datetime.now() - timedelta(days=7))
        # postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d %H:%M"))

        if date == "Just added" or date == "Today":
            date = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d %H:%M"))

        if company == False:
            company = None
        # if age <= postDate and url not in scraped:
        data.append({
            "timestamp": date,
            "title": title,
            "company": company,
            "url": url,
            "area": area,
            "category": "job"
        })
        # print(f"indeed: Added {title}")
        scraped.add(url)
        print(data)

def getResults(item):
    # print(item)
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all("div", {"class": "jobsearch-SerpJobCard unifiedRow row result clickcard"})
    print(results)
    getJobs(results)

def getURL(items):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    # ua=UserAgent()
    # hdr = {'User-Agent': ua.random,
    #   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    #   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    #   'Accept-Encoding': 'none',
    #   'Accept-Language': 'en-US,en;q=0.8',
    #   'Connection': 'keep-alive'
    # }

    # for code in items:
    url = f"https://www.indeed.com/jobs?q=Developer&l=94043&radius=50&sort=date&remotejob=032b3046-06a3-4876-8dfd-474eb5e7ed11"
    response = requests.get(url=url, headers=headers).text
    getResults(response)
    print(response)

def main():
    getURL(codes)
    createJSON(data)

main()

sys.exit(0)