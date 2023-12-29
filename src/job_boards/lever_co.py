import requests
import sys
import json
import time
import random
from datetime import datetime
from lxml import html
sys.path.insert(0, ".")
from src.job_boards.helpers import ProcessCompanyJobData, user_agents


process_data = ProcessCompanyJobData()
FILE_PATH = "src/data/params/lever_co.txt"


def get_results(item: str, param: str):
    source_url = f"https://jobs.lever.co/{param}"
    company_name = param.capitalize()
    logo = None
    lever = "src/data/assets/lever_assets.txt"
    table = process_data.get_stored_data(lever)
    if param in table:
        company_name = table[param]["name"] 
        logo = table[param]["logo"]
    else:
        try:
            r = requests.get(source_url)
            tree = html.fromstring(r.content)
            logo = tree.xpath("//a[@class='main-header-logo']/img/@src")[0]
            company_name = tree.xpath("//head/title/text()")[0]
            with open(lever, "a") as a:
                a.write(f"{param}`{company_name}`{logo}\n")
        except Exception as e:
            print(f"=> lever.co: Failed to get logo for {param}. Error: {e}.")
    for i in item:
        # use true division by 1e3 (float 1000)
        date = datetime.fromtimestamp(i["createdAt"] / 1e3)
        post_date = datetime.timestamp(
            datetime.strptime(str(date).rsplit(".")[0], "%Y-%m-%d %H:%M:%S"))
        apply_url = i["hostedUrl"].strip()
        description = i["descriptionPlain"]
        position = i["text"].strip()
        location = i["categories"]["location"].strip() if "location" in i["categories"] else "See description"
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
        headers = {"User-Agent": random.choice(user_agents)}
        url = f"https://api.lever.co/v0/postings/{company}/"
        response = requests.get(url, headers=headers)
        
        try:
            if response.ok:
                data = json.loads(response.text)
                get_results(data, company)
                if count % 20 == 0:
                    time.sleep(10)
                else:
                    time.sleep(0.2)
            elif response.status_code == 404:
                process_data.remove_not_found(FILE_PATH, company)
            count += 1
        except Exception as e:
            if response.status_code == 429:
                print(
                    f"=> lever.co: Failed to scrape {company}. Status code: {response.status_code}.")
                break
            else:
                print(
                    f"=> lever.co: Failed for {company}. Status code: {response.status_code}. Error: {e}.")


def main():
    companies = process_data.read_list_of_companies(FILE_PATH)
    get_url(companies)


if __name__ == "__main__":
    main()