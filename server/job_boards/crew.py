import requests
import sys
import json
import time
import random
from datetime import datetime
from .helpers import headers as h
from .helpers.classes import FilterJobs, RemoveNotFound, ReadListOfCompanies


FILE_PATH = "./data/params/crew.txt"


def get_results(item: str, param: str):
    source_url = f"https://{param}.crew.work/jobs"
    company_name = item["name"]
    logo = item.get("logo")

    for i in item["jobs"]:
        date = datetime.strptime(i["updatedAt"].rsplit(".")[0], "%Y-%m-%dT%H:%M:%S")
        post_date = datetime.timestamp(
            datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S"))
        apply_url = f"{source_url}/{i['id']}"
        # description = i["description"]
        position = i["name"].strip()
        location = i["location"].strip()

        FilterJobs({
            "timestamp": post_date,
            "title": position,
            "company": company_name,
            "company_logo": logo,
            #"description": description,
            "url": apply_url,
            "location": location,
            "source": company_name,
            "source_url": source_url
        })


def get_url(companies: list):
    count = 0
    for company in companies:
        try:
            headers = {"User-Agent": random.choice(h.headers)}
            url = f"https://{company}.crew.work/assets/company.json"
            response = requests.get(url, headers=headers)

            if response.ok:
                data = json.loads(response.content)
                get_results(data, company)
                if count % 20 == 0:
                    time.sleep(10)
                else:
                    time.sleep(0.2)
            elif response.status_code == 404:
                RemoveNotFound(FILE_PATH, company)
            count += 1

        except Exception as e:
            if response.status_code == 429:
                print(
                    f"=> crew.work: Failed to scrape {company}. Status code: {response.status_code}.")
                break
            else:
                print(
                    f"=> crew.work: Failed for {company}. Status code: {response.status_code}. Error: {e}.")


def main():
    companies = ReadListOfCompanies(FILE_PATH)
    get_url(companies)


# if __name__ == "__main__":
#     main()
#     sys.exit(0)
