from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests, sys, re
from .modules import create_temp_json
# import modules.create_temp_json as create_temp_json


data = create_temp_json.data
scraped = create_temp_json.scraped

f = open(f"./data/params/greenhouse_io.txt", "r")
companies = [company.strip() for company in f]
f.close()

def getJobs(item, company, name):
    for job in item:
        date = datetime.strftime(datetime.now(), "%Y-%m-%d")
        title = job.find("a", href=True).text.strip()
        company = company.strip()
        url = "https://boards.greenhouse.io"+job.find("a", href=True)["href"]
        location = job.find("span", {"class": "location"}).text.strip()

        # print(date, title, company, url, location)
        postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d"))

        if url not in scraped:
            data.append({
                "timestamp": postDate,
                "title": title,
                "company": company,
                "url": url,
                "location": location,
                "source": company,
                "source_url": f"https://boards.greenhouse.io/{name}",
                "category": "job"
            })
            scraped.add(url)
            print(f"=> greenhouse.io: Added {title} for {company}")
        else:
            print(f"=> greenhouse.io: Already scraped {title} for {company}")


def getResults(item, name):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all("section", {"class": "level-0"})
    company = soup.find("title").text.replace("Jobs at", "") if "Jobs at" in soup.find("title").text else name.capitalize()

    for result in results:
        r = result.find(re.compile("^h[2-4]$")).text.strip()

        if r == "Engineering" or r == "Technology":
            results = result.find_all("div", {"class": "opening"})
            # print(results)

    # print(company)
    getJobs(results, company, name)
    # print(results)

def getURL():
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0"}

    for name in companies:
        try:
            url = f"https://boards.greenhouse.io/{name}"
            response = requests.get(url, headers=headers).text
            getResults(response, name)
            
            # print(response)
        except:
            print(f"=> greenhouse.io: Failed to scrape {name}. Continue to next")
            continue


def main():
    getURL()

# main()
# sys.exit(0)