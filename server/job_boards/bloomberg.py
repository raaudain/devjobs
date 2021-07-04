from datetime import datetime
import requests, json, sys
# from .modules import create_temp_json
import modules.create_temp_json as create_temp_json


data = create_temp_json.data

def getJobs(url, company, position, location):
    date = datetime.strftime(datetime.now(), "%Y-%m-%d")
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
        "source": "HireArt",
        "source_url": "https://www.hireart.com",
        "category": "job"
    })
    print(f"=> hireart: Added {title} for {company}")


def getResults(item):
    jobs = item["jobData"]
    for data in jobs:
        date = data["PostedDate"]
        apply_url = data["apply_url"].strip()
        company_name = data["company_name"].strip()
        position = data["JobTitle"].strip()
        city = data["City"].strip()
        state = f"{data['State'].strip() if data['State'] is not '' else None}, "
        country = data["Country"].strip()
        locations_string = f"{city}, {state}{country}"
        print(date, apply_url, company_name, position, locations_string)

def getURL():
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0", "X-Requested-With": "XMLHttpRequest"}

    url = f"https://careers.bloomberg.com/job_search/search_query?autocompleteTags=%5B%5D&selectedFilterFields=%5B%7B%22name%22%3A%22Engineering%22%2C%22parentFacet%22%3A%22Business+area%22%7D%5D&jobStartIndex=0&jobBatchSize=1000"
    response = requests.get(url, headers=headers).text

    data = json.loads(response)

    getResults(data)
    
    # print(data)
     


def main():
    getURL()

main()
sys.exit(0)

