from datetime import datetime
import requests, json, sys, time
from .modules import create_temp_json
# import modules.create_temp_json as create_temp_json


data = create_temp_json.data

def getJobs(date, url, company, position, location):
    date = date
    title = position
    company = company
    url = url
    location = location

    # print(date, title, company, url, location)
    postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d"))
    
    data.append({
        "timestamp": postDate,
        "title": title,
        "company": company,
        "url": url,
        "location": location,
        "source": "Bloomberg",
        "source_url": "https://www.bloomberg.com/company/what-we-do/",
        "category": "job"
    })
    print(f"=> bloomberg: Added {title} for {company}")


def getResults(item):
    date = item["datePosted"]
    apply_url = item["url"]
    company_name = "Bloomberg"
    position = item["jobTitle"]
    locations_string = item["jobLocation"]

    getJobs(date, apply_url, company_name, position, locations_string)

def getURL():
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0", "X-Requested-With": "XMLHttpRequest"}

    url1 = f"https://careers.bloomberg.com/job_search/search_query?autocompleteTags=%5B%5D&selectedFilterFields=%5B%7B%22name%22%3A%22Software+Developer%2FEngineering%22%2C%22count%22%3A%22239%22%2C%22isSelected%22%3Atrue%2C%22parentFacet%22%3A%22Job+function%22%2C%22id%22%3A%22c41%22%7D%2C%7B%22name%22%3A%22Technical+Support%22%2C%22count%22%3A%2216%22%2C%22isSelected%22%3Atrue%2C%22parentFacet%22%3A%22Job+function%22%2C%22id%22%3A%22c48%22%7D%5D&jobStartIndex=0&jobBatchSize=1000"
    response = requests.get(url1, headers=headers).text
    data = json.loads(response)
    jobID = []

    for d in data["jobData"]:
        if "engineer" in d["Specialty"]["Value"].lower() or "tech" in d["Specialty"]["Value"].lower():
            jobID.append(d["JobReqNbr"])
    
    count = 1

    for j in jobID:
        url2 = f"https://careers.bloomberg.com/job_search/detail_query?jobID={j}"
        res = requests.get(url2, headers=headers).text
        post = json.loads(res)

        getResults(post)

        if count % 5 == 0:
            time.sleep(5)
                
        count+=1


def main():
    getURL()

# main()
# sys.exit(0)

