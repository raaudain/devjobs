import requests
import sys
import time
import random
from datetime import datetime
sys.path.insert(0, ".")
from src.job_boards.helpers import user_agents, ProcessCompanyJobData


process_data = ProcessCompanyJobData()
FILE_PATH = "src/data/params/bamboohr.txt"


def get_results(item: str, param: str):
    headers = {"User-Agent": random.choice(user_agents)}
    r = requests.get(f"https://{param}.bamboohr.com/careers/company-info", headers=headers)
    logo = r.json()["result"]["shareImageUrl"]
    company = r.json()["result"]["name"]

    for d in item["result"]:
        date = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
        post_date = datetime.timestamp(datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S"))
        apply_url = f"https://{param}.bamboohr.com/careers/{d['id']}"
        position = d["jobOpeningName"].strip()
        location = f"{d['location']['city'].strip()}, {d['location']['state'].strip() if d['location']['state'] else d['location']['country'].strip()}"
        process_data.filter_jobs({
            "timestamp": post_date,
            "title": position,
            "company": company,
            "company_logo": logo,
            "url": apply_url,
            "location": location,
            "source": company,
            "source_url": f"https://{param}.bamboohr.com/careers"
        })


def get_url(companies: list):
    page = 1
    for company in companies:
        try:
            headers = {"User-Agent": random.choice(user_agents)}
            url = f"https://{company}.bamboohr.com/careers/list"
            response = requests.get(url, headers=headers)
            if response.ok:
                get_results(response.json(), company)
                if page % 20 == 0:
                    time.sleep(5)
                else:
                    time.sleep(0.2)
                page += 1
            elif response.status_code == 404:
                process_data.remove_not_found(FILE_PATH, company)
        except Exception as e:
            if response.status_code == 429:
                print(
                    f"=> bamboohr: Failed to scrape {company}. Error: {e}.")
                break
            else:
                print(f"=> bamboohr: Failed to scrape {company}. Error: {e}.")


def main():
    companies = process_data.read_list_of_companies(FILE_PATH)
    get_url(companies)


if __name__ == "__main__":
    main()

