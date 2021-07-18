from datetime import datetime
import requests, json, sys
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
        "url": url,
        "location": location,
        "source": company,
        "source_url": "https://careers.nintendo.com",
        "category": "job"
    })
    print(f"=> nintendo: Added {title} for {company}")


def getResults(item):
    for data in item:
        if "Software" in data["JobDescription"] or "IT " in data["JobTitle"] or "Support" in data["JobTitle"]:
            date = datetime.strptime(data["JobCreationDate"], "%B %d, %Y")
            job_id = data["JobId"]
            apply_url = f"https://careers.nintendo.com/job-openings/listing/{job_id}.html"
            company_name = "Nintendo of America"
            position = data["JobTitle"].strip()
            locations_string = f"{data['JobPrimaryLocationCode']}, {data['JobLocationStateAbbrev']}".strip()
            
            getJobs(date, apply_url, company_name, position, locations_string)
        

def getURL():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36", "Origin": "https://careers.nintendo.com"}

    url = f"https://2oc84v7py6.execute-api.us-west-2.amazonaws.com/prod/api/jobs/"

    response = requests.get(url, headers=headers).text
    data = json.loads(response)

    getResults(data)
    
    # print(data)
     


def main():
    getURL()

# main()
# sys.exit(0)