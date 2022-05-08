from datetime import datetime
import sys
import feedparser
from .modules.classes import Filter_Jobs, Read_List_Of_Companies, Remove_Not_Found
# import modules.create_temp_json as create_temp_json


FILE_PATH = "./data/params/recruiterbox.txt"


def get_results(item: str, name: str):
    company_name = item["channel"]["title"].replace("Jobs at", "").strip()
    data = item["entries"]
    for i in data:
        date = i["published"]
        post_date = datetime.timestamp(datetime.strptime(
            str(date), "%a, %d %b %Y %H:%M:%S %z"))
        apply_url = i["link"]
        position = i["title"]
        city = "Remote" if "UTC" in i["job_locationcity"] or "Global" in i[
            "job_locationcity"] else f'{i["job_locationcity"]}'
        region = f', {i["job_locationstate"]}' if i["job_locationstate"] else ""
        country = f', {i["job_locationcountry"]}' if i["job_locationcountry"] else ""
        location = f"{city}{region}{country}"
        source_url = f"https://{name}.recruiterbox.com/jobs"
        Filter_Jobs({
            "timestamp": post_date,
            "title": position,
            "company": company_name,
            "url": apply_url,
            "location": location,
            "source": company_name,
            "source_url": source_url
        })


def get_url(companies: list):
    for company in companies:
        url = f"http://recruiterbox.com/jobfeeds/{company}"
        response = feedparser.parse(url)
        # bozo flag checks if a feed is malformed
        if response.bozo == False:
            get_results(response, company)
        elif response.status == 404:
            Remove_Not_Found(FILE_PATH, company)
        else:
            error = response.bozo_exception
            print(f"=> recruiterbox: Failed {company}. Error: {error}")


def main():
    companies = Read_List_Of_Companies(FILE_PATH)
    get_url(companies)


# main()
# sys.exit(0)
