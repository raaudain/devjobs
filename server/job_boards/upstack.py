import requests, json, sys, random
from datetime import datetime
# from .modules import create_temp_json
# from .modules import headers as h
import modules.create_temp_json as create_temp_json
import modules.headers as h


def get_jobs(url: str, company: str, position: str, location: str):
    data = create_temp_json.data

    date = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
    post_date = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))
    
    data.append({
        "timestamp": post_date,
        "title": position,
        # "qualifications": qualifications,
        "company": company,
        "company_logo": "https://res-5.cloudinary.com/crunchbase-production/image/upload/c_lpad,h_256,w_256,f_auto,q_auto:eco/wtwdopjgymgpcawhfm0z",
        "url": url,
        "location": location,
        "source": company,
        "source_url": "https://upstack.co/careers",
        "category": "job"
    })
    print(f"=> hireart: Added {position} for {company}")

def get_results(item: str):
    jobs = item["job_openings"]
    print(jobs)

    for data in jobs:
        apply_url = ""
        company_name = "Upstack"
        position = data["title"].strip()
        locations_string = data["location"].strip()
        print(apply_url, company_name, position, locations_string)

def get_url():
    headers = {"User-Agent": random.choice(h.headers)}
    url = "https://api.upstack.co/careers"
    response = requests.get(url, headers=headers)

    if response.ok:
        data = json.loads(response.text)
        get_results(data)
    else:
        print("=> hireart: Error - Response status", response.status_code)

def main():
    get_url()


main()
sys.exit(0)