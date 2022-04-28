import requests, json, sys, time, random
from datetime import datetime
from .modules import create_temp_json
from .modules import headers as h
# import modules.create_temp_json as create_temp_json
# import modules.headers as h


def get_jobs(date: str, url: str, company: str, position: str, location: str):
    data = create_temp_json.data
    scraped = create_temp_json.scraped

    post_date = datetime.timestamp(datetime.strptime(str(date), "%Y-%m-%dT%H:%M:%S%z"))
    
    data.append({
        "timestamp": post_date,
        "title": position,
        "company": company,
        "company_logo": "https://www.indeed.jobs/wp-content/uploads/2021/02/indeed-logo-2021.svg",
        "url": url,
        "location": location,
        "source": company,
        "source_url": "https://search.indeed.jobs/main/jobs",
        "category": "job"
    })
    scraped.add(company)
    print(f"=> indeed: Added {position}")


def get_results(item: str):
    jobs = item["jobs"]

    for j in jobs:
        if "Engineer" in j["data"]["title"] or "Data" in j["data"]["title"] or "Support" in j["data"]["title"] or "IT " in j["data"]["title"] or "Programmer" in j["data"]["title"] or "QA" in j["data"]["title"] or "Software" in j["data"]["title"]  or "Tech " in j["data"]["title"] or "Help" in j["data"]["title"] or "Desk" in j["data"]["title"] or "Developer" in j["data"]["title"] and ("Mechnicial" not in j["data"]["title"] and "Electrical" not in j["data"]["title"] and "Front Desk" not in j["data"]["title"]):
            date = j["data"]["create_date"]
            position = j["data"]["title"].strip()
            company_name = "Indeed"
            apply_url = "https://search.indeed.jobs/main/jobs/"+j["data"]["req_id"].strip()
            locations_string = j["data"]["full_location"].strip()

            get_jobs(date, apply_url, company_name, position, locations_string)


def get_url():
        try:
            headers = {"User-Agent": random.choice(h.headers)}
            url = f"https://www.diversifytech.co/page-data/job-board/page-data.json"
            response = requests.get(url, headers=headers)
            data = json.loads(response.text)["result"]["data"]["allAirtable"]["edges"]

            if len(data["jobs"]) > 0:               
                get_results(data)         
        except:
            print(f"=> diversify: Status code: {response.status_code}.")



def main():
    get_url()


# main()
# sys.exit(0)