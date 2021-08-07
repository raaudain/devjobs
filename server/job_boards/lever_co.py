from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests, sys, time, json
from .modules import create_temp_json
# import modules.create_temp_json as create_temp_json


data = create_temp_json.data
scraped = create_temp_json.scraped

f = open(f"./data/params/lever_co.txt", "r")
companies = [company.strip() for company in f]
f.close()

def getJobs(item, company, source_url):
    for job in item:
        date = datetime.strftime(datetime.now(), "%Y-%m-%d")
        title = job.find("h5", {"data-qa": "posting-name"}).text
        company = company
        url = job["href"]
        location = job.find("span", {"class": "sort-by-location posting-category small-category-label"}).text

        # print(date, title, company, url, location, source_url)
        postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d"))

        if url not in scraped:
            data.append({
                "timestamp": postDate,
                "title": title,
                "company": company,
                "url": url,
                "location": location,
                "source": company,
                "source_url": source_url,
                "category": "job"
            })
            scraped.add(url)
            scraped.add(company)
            print(f"=> lever.co: Added {title} for {company}")
        else:
            print(f"=> lever.co: Already scraped {title} for {company}")
        

def getResults(item, name):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all("a", {"class": "posting-title"})
    company = soup.find("title").text.strip()
    source_url = f"https://jobs.lever.co/{name}"

    postings = []

    for result in results:
        h5 = result.find("h5", {"data-qa":"posting-name"}).text
        if "Engineer" in h5 or "Tech" in h5 or "Web" in h5 or "Data " in h5:
            postings.append(result)

    results = postings

    getJobs(results, company, source_url)
    # print(results)

def getURL():
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0"}

    # url = f"https://jobs.lever.co/clubhouse"
    # response = requests.get(url, headers=headers).text
    # getResults(response)
    count = 1

    for name in companies:
        try:
            url = f"https://jobs.lever.co/{name}"
            response = requests.get(url, headers=headers).text
            getResults(response, name)
            
            if count % 5 == 0:
                time.sleep(5)
                
            count+=1
            # print(response)
        except:
            print(f"=> lever_co: Scrape failed for {name}. Going to next.")
            continue


def main():
    getURL()

# main()
# sys.exit(0)