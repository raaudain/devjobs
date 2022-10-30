import requests
import json
import sys
import time
import random
from lxml import html
from datetime import datetime
sys.path.insert(0, ".")
from server.job_boards.helpers import headers as h
from server.job_boards.helpers.classes import ProcessCompanyJobData
# import modules.headers as h
# import modules.classes as c


process_data = ProcessCompanyJobData()
FILE_PATH = "server/data/params/polymer.txt"


def get_results(item: str, param: str):
    wrk = "server/data/assets/polymer_assets.txt"
    source_url = f"https://jobs.polymer.co/{param}"
    logo = None
    table = process_data.get_stored_data(wrk)
    if param in table:
        logo = table[param]["logo"]
    else:
        try:
            r = requests.get(source_url)
            tree = html.fromstring(r.content)
            logo = tree.xpath("//div[@class='header__logo']/img/@src")[0]
            with open(wrk, "a") as a:
                a.write(f"{param}`n/a`{logo}\n")
        except Exception as e:
            print(f"=> wrk: Error getting logo for {param}. {e}.")
    jobs = item["items"]
    for j in jobs:
        date = j["published_at"]
        post_date = datetime.timestamp(
            datetime.strptime(str(date), "%Y-%m-%dT%H:%M:%S.%fZ"))
        position = j["title"].strip()
        company_name = j["organization_name"].strip()
        apply_url = j["job_post_url"].strip()
        city = f"{j['city'].strip()}, " if j['city'] else ""
        state = f"{j['state_region'].strip()}, " if j["state_region"] else ""
        country = f"{j['country'].strip()}" if j["country"] else ""
        remote = f" | {j['remoteness_pretty'].strip()}" if j["remoteness_pretty"] and "No" not in j["remoteness_pretty"] else ""
        location = city+state+country+remote
        process_data.filter_jobs({
            "timestamp": post_date,
            "title": position,
            "company": company_name,
            "company_logo": logo,
            "url": apply_url,
            "location": location,
            "source": company_name,
            "source_url": source_url
        })


def get_url(companies: list):
    count = 1
    for company in companies:
        try:
            headers = {"User-Agent": random.choice(h.headers)}
            url = f"https://jobs.polymer.co/api/v1/public/organizations/{company}/jobs/"
            response = requests.get(url, headers=headers)
            if response.ok:
                data = json.loads(response.text)
                get_results(data, company)
                if count % 20 == 0:
                    time.sleep(5)
                else:
                    time.sleep(0.2)
                count += 1
            elif response.status_code == 404:
                process_data.remove_not_found(FILE_PATH, company)
            else:
                print(f"=> polymer: Status code {response.status_code} for {company}")
        except Exception as e:
            print(f"=> polymer: Error for {company}. {e}")


def main():
    companies = process_data.read_list_of_companies(FILE_PATH)
    get_url(companies)


# main()
# sys.exit(0)
