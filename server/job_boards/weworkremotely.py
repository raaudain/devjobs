from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from .modules import create_temp_json
# import modules.create_temp_json as create_temp_json
import json, requests, sys


data = create_temp_json.data

def getJobs(item):
    for job in item:
        try:
            date = job.find("time")
            title = job.find("span", {"class": "title"}).text
            company = job.find("span", {"class": "company"}).text
            url = "https://www.weworkremotely.com"+job.find_all("a", href=True)[1]["href"]
            location = job.find("span", {"class": "region company"})
            
            if location:
                location = job.find("span", {"class": "region company"}).contents[0]
            else:
                location = "Remote"

            if date:
                date = job.find("time")["datetime"].replace("T", " ").replace("Z", "")[:-3]
            else:
                date = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M")

            age = datetime.timestamp(datetime.now() - timedelta(days=14))
            postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d %H:%M"))

            if age <= postDate:
                data.append({
                    "timestamp": postDate,
                    "title": title,
                    "company": company,
                    "url": url,
                    "location": location,
                    "source": "WeWorkRemotely",
                    "source_url": "https://weworkremotely.com/",
                    "category": "job"
                })
            print(f"=> weworkremotely: Added {title}")
        except:
            print(f"Error for {item}")
            pass

def getResults(item):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find("div", {"class": "content"}).find_all("li", {"class": ["feature",""]})
    getJobs(results)

def getURL():
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}
    url = f"https://weworkremotely.com/remote-jobs/search?term=&button=&categories%5B%5D=2&categories%5B%5D=17&categories%5B%5D=18&categories%5B%5D=6"
    response = requests.get(url, headers=headers)

    if response.ok:
        getResults(response.text)
    else:
        print("=> weworkremotely: Error - Response status", response.status_code)

def main():
    getURL()


# main()

# sys.exit(0)