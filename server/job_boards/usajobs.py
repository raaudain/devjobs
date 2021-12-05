from datetime import datetime
import requests, json, sys, time
from .modules import create_temp_json
# import modules.create_temp_json as create_temp_json


data = create_temp_json.data

def getJobs(date, url, company, position, location):
    date = str(date)
    title = position
    company = company
    url = url
    location = location

    # print(date, title, company, url, location)

    postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))
    
    data.append({
        "timestamp": postDate,
        "title": title,
        "company": company,
        "company_logo": "https://careersourcefloridacrown.com/wp-content/uploads/2017/06/usajobs.png",
        "url": url,
        "location": location,
        "source": "USAJobs",
        "source_url": "https://www.usajobs.gov/",
        "category": "job"
    })
    print(f"=> usajobs: Added {title} for {company}")


def getResults(item):
    jobs = item["Jobs"]

    # print(jobs)

    for data in jobs:
        if "Software" in data["Title"] or "IT " in data["Title"] or "Information Technology" in data["Title"] or "Computer Engineer" in data["Title"] or "Network Engineer" in data["Title"]:
            date = datetime.strptime(data["DateDisplay"][:13][5:], "%m/%d/%y")
            apply_url = data["PositionURI"]
            company_name = data["Agency"].strip()
            position = data["Title"].strip()
            locations_string = data["Location"].strip()
            
            getJobs(date, apply_url, company_name, position, locations_string)
        

def getURL():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"}

    page = 1

    while page < 50:
        try:
            url = "https://www.usajobs.gov/Search/ExecuteSearch"
            payload = {
                "HiringPath": ["public"],
                "Page": page,
                "Keyword": "software",
                "UniqueSearchID": "162dbbf5-6795-4786-840e-efd686188e29",
                "IsAuthenticated": False
            }

            response = requests.post(url, json=payload, headers=headers).text

            data = json.loads(response)

            getResults(data)

            if page % 5 == 0:
                time.sleep(5)
            
            page+=1
        except:
            print(f"=> usajobs: Failed to scrap page {page}")
            continue
    # print(data)
     


def main():
    getURL()

# main()
# sys.exit(0)