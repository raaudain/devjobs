from datetime import datetime
import requests, json, sys
from .modules import create_temp_json
# import modules.create_temp_json as create_temp_json


def get_jobs(date: str, url: str, company: str, position: str, location: str):
    data = create_temp_json.data
    postDate = datetime.timestamp(datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S"))
    
    data.append({
        "timestamp": postDate,
        "title": position,
        "company": company,
        "url": url,
        "location": location,
        "source": "Zillow Group",
        "source_url": "https://www.zillow.com/careers/",
        "category": "job"
    })
    print(f"=> zillow: Added {position} for {company}")


def get_results(item: str):
    jobs = item["Data"]

    for data in jobs:
        date = datetime.strptime(data["AddedOn"], "%m/%d/%Y %I:%M:%S %p")
        job_id = data["JobId"]
        url_job_title = data["UrlJobTitle"].replace("-", "").replace(",", "")
        apply_url = f"https://careers.zillowgroup.com/ShowJob/JobId/{job_id}/{url_job_title}"
        company_name = data["ShortTextField6"].strip()
        position = data["JobTitle"].strip()
        locations_string = data["LongTextField2"].strip()
        
        get_jobs(date, apply_url, company_name, position, locations_string)
        

def get_url():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36", "Origin": "https://careers.zillowgroup.com"}
    url = f"https://cmsservice.smashfly.com/api/jobs/v1/jobs/hZtAUIBJAtYt3u6LLr6IZa1u7mwk0XfZo2hvMFcZglTioUuFr6MJtKuxbFw_h2spRH7NzzVPY181?sort=AddedOn-desc&page=1&pageSize=1000&group=&filter=ShortTextField1~eq~%27Data%20Science%20%26%20Analytics%27~or~ShortTextField1~eq~%27IT%20Operations%27~or~ShortTextField1~eq~%27Software%20Development%27&fields=JobTitle%2CShortTextField1%2CShortTextField6%2CLongTextField2%2CShortTextField13%2CUrlJobTitle"
    response = requests.get(url, headers=headers)

    if response.ok:
        data = json.loads(response.text)
        get_results(data)
    else:
        print("=> zillow: Error - Response status", response.status_code)


def main():
    get_url()


# main()
# sys.exit(0)