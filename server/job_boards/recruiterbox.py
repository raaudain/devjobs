from datetime import datetime
import sys, feedparser
from .modules import create_temp_json
# import modules.create_temp_json as create_temp_json


def get_jobs(date: str, url: str, company: str, position: str, location: str, source_url: str):
    data = create_temp_json.data
    postDate = datetime.timestamp(datetime.strptime(str(date), "%a, %d %b %Y %H:%M:%S %z"))

    data.append({
        "timestamp": postDate,
        "title": position,
        "company": company,
        "url": url,
        "location": location,
        "source": company,
        "source_url": source_url,
        "category": "job"
    })
    print(f"=> recruiterbox: Added {position} for {company}")


def get_results(item: str, name: str):
    company_name = item["channel"]["title"].replace("Jobs at", "").strip()
    data = item["entries"]

    for i in data:
        if ("Engineer" in i["title"] or "IT" in i["title"] or "Programmer" in i["title"] or "Data" in i["title"] or "Help" in i["title"] or "Desk" in i["title"] or "Developer" in i["title"]) and ("structural" not in i["title"].lower() or "Bridge" not in i["title"] or "mechanical" not in i["title"].lower() or "material" not in i["title"].lower() or "civil" not in i["title"].lower()):
            date = i["published"]
            apply_url = i["link"]
            position = i["title"]
            city = "Remote" if "UTC" in i["job_locationcity"] or "Global" in i["job_locationcity"] else f'{i["job_locationcity"]}'
            region = f', {i["job_locationstate"]}' if i["job_locationstate"] else ""
            country = f', {i["job_locationcountry"]}' if i["job_locationcountry"] else ""
            locations_string = f"{city}{region}{country}"
            source_url = f"https://{name}.recruiterbox.com/jobs"

            get_jobs(date, apply_url, company_name, position, locations_string, source_url)


def get_url(companies: list):
    for company in companies:
        url = f"http://recruiterbox.com/jobfeeds/{company}"
        response = feedparser.parse(url)

        if response.bozo: get_results(response, company)
        else: print(f"=> recruiterbox: Failed {company}. {response.bozo_exception}")


def main():
    f = open(f"./data/params/recruiterbox.txt", "r")
    companies = [company.strip() for company in f]
    f.close()

    get_url(companies)

# main()
# sys.exit(0)