import requests
import json
import sys
import time
import random
from datetime import datetime
from .modules.classes import Filter_Jobs
from .modules import create_temp_json
from .modules import headers as h

# import modules.create_temp_json as create_temp_json
# import modules.headers as h
# import modules.classes as c


def get_jobs(date: str, url: str, company: str, position: str, location: str):
    data = create_temp_json.data
    scraped = create_temp_json.scraped
    # data = Create_Temp_JSON.data
    # scraped = Create_Temp_JSON.scraped

    post_date = datetime.timestamp(
        datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S"))

    if url not in scraped:
        data.append({
            "timestamp": post_date,
            "title": position,
            # "qualifications": qualifications,
            "company": company,
            "company_logo": "https://tauchcomputertest.de/wp-content/uploads/2016/11/Amazon-Logo.png",
            "url": url,
            "location": location,
            "source": "Amazon",
            "source_url": "https://www.amazon.jobs",
            "category": "job"
        })
        print(f"=> amazon: Added {position} for {company}")
        scraped.add(url)


def get_results(item: str):
    data = item["jobs"]
    for d in data:
        # if "Engineer" in d["title"] or "Data" in d["title"] or "Tech " in d["title"] or "IT" in d["title"] or "Support" in d["title"]:
        date = datetime.strptime(d["posted_date"], "%B %d, %Y")
        post_date = datetime.timestamp(
            datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S"))
        position = d["title"]
        # desc = d["preferred_qualifications"].replace("· ", "").replace("• ", "").split("<br/>")
        company_name = d["company_name"]
        job_path = d["job_path"].strip()
        apply_url = f"https://amazon.jobs{job_path}"
        location = d["normalized_location"]

        # get_jobs(date, apply_url, company_name, position, locations_string)
        Filter_Jobs({
            "timestamp": post_date,
            "title": position,
            "company": company_name,
            "company_logo": "https://tauchcomputertest.de/wp-content/uploads/2016/11/Amazon-Logo.png",
            "url": apply_url,
            "location": location,
            "source": "Amazon",
            "source_url": "https://www.amazon.jobs",
        })

        # get_job = Handle_Jobs(date, apply_url, company_name, position, locations_string, "Amazon", "https://www.amazon.jobs", "amazon")
        # get_job.add_job()


def get_url():
    page = 0
    try:
        while page <= 10:
            headers = {"User-Agent": random.choice(h.headers)}
            url = f"https://amazon.jobs/en/search.json?category[]=software-development&category[]=solutions-architect&category[]=operations-it-support-engineering&category[]=project-program-product-management-technical&category[]=systems-quality-security-engineering&category[]=machine-learning-science&result_limit=100&sort=relevant&offset={page}0"
            response = requests.get(url, headers=headers)
            if response.ok:
                data = json.loads(response.text)
                get_results(data)
                if page % 10 == 0:
                    time.sleep(5)
                page += 1
            else:
                print(
                    f"=> amazon: Failed on page {page}. Status code: {response.status_code}.")
                break
    except:
        print(f"=> amazon: Amazon failed")


def main():
    get_url()


# main()
# sys.exit(0)
