from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests, sys, time
# from .modules import create_temp_json
import modules.create_temp_json as create_temp_json


data = create_temp_json.data

f = open(f"./data/params/jobvite.txt", "r")
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
        
        print(f"=> jobvite: Added {title} for {company}")

        

def getResults(item, name):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all("tr")
    company = name.capitalize()
    source_url = f"https://jobs.lever.co/{name}"

    postings = []

    for result in results:
        print(result.find("td", class_="jv-job-list-name").text.strip(), name)
        print(result.find("td", class_="jv-job-list-location").text.strip())
        # title = result.find(class_="jv-job-list-name").text
        # if "Engineer" in title or "Tech" in title or "Web" in title or "Data " in title or "QA" in title or "Cloud" in title or "IT " in title:
        #     print(result)

    # results = postings

    # getJobs(results, company, source_url)
    # print(results)

def getURL():
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0"}

    # url = f"https://jobs.lever.co/clubhouse"
    # response = requests.get(url, headers=headers).text
    # getResults(response)
    count = 1

    for name in companies:
        # try:
        url = f"https://jobs.jobvite.com/careers/{name}"
        response = requests.get(url, headers=headers).text
        getResults(response, name)
        
        if count % 10 == 0:
            time.sleep(5)
            
        count+=1
            # print(response)
        # except:
        #     print(f"=> jobvite: Scrape failed for {name}. Going to next.")
        #     continue


def main():
    getURL()

main()
sys.exit(0)