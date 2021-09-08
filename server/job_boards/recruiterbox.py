from datetime import datetime
import sys, feedparser
from .modules import create_temp_json
# import modules.create_temp_json as create_temp_json


data = create_temp_json.data

f = open(f"./data/params/recruiterbox.txt", "r")
companies = [company.strip() for company in f]
f.close()

def getJobs(date, url, company, position, location, source_url):
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


def getResults(item, name):
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

            getJobs(date, apply_url, company_name, position, locations_string, source_url)


def getURL():
    for company in companies:
        try:
            url = f"http://recruiterbox.com/jobfeeds/{company}"
            response = feedparser.parse(url)

            getResults(response, company)
        except:
            print(f"=> recruiterbox: Failed {company}")
            continue


def main():
    getURL()

# main()
# sys.exit(0)