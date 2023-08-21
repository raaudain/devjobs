import requests
import sys
import json
import time
import random
from datetime import datetime
sys.path.insert(0, ".")
from src.job_boards.helpers import ProcessCompanyJobData, date_formatter, user_agents


process_data = ProcessCompanyJobData()
FILE_PATH = "src/data/params/crew.txt"

def get_results(item: str, param: str):
    source_url = f"https://{param}.crew.work/jobs"
    company_name = item["name"]
    logo = item.get("logo")

    for i in item["jobs"]:
        date = date_formatter(i["updatedAt"])
        post_date = datetime.timestamp(
            datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S"))
        apply_url = f"{source_url}/{i['id']}"
        # description = i["description"]
        position = i["name"].strip()
        location = i["location"].strip()

        process_data.filter_jobs({
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
            headers = {"User-Agent": random.choice(user_agents)}
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
                process_data.remove_not_found(FILE_PATH, company)
            count += 1

        except Exception as e:
            print(
                f"=> crew.work: Failed for {company}. Error: {e}.")


def main():
    companies = process_data.read_list_of_companies(FILE_PATH)
    get_url(companies)


if __name__ == "__main__":
    main()
