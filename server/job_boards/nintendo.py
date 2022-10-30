import requests
import json
import sys
import random
from datetime import datetime
from bs4 import BeautifulSoup
sys.path.insert(0, ".")
from server.job_boards.helpers import headers as h
from server.job_boards.helpers.classes import ProcessCompanyJobData
# import modules.create_temp_json as create_temp_json


process_data = ProcessCompanyJobData()

def get_results(item: str):
    for data in item:
        date = datetime.strptime(data["JobCreationDate"], "%B %d, %Y")
        post_date = datetime.timestamp(
            datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S"))
        job_id = data["JobId"]
        apply_url = f"https://careers.nintendo.com/job-openings/listing/{job_id}.html"
        company_name = "Nintendo of America"
        position = data["JobTitle"].strip()
        # results = BeautifulSoup(data["ExternalQualificationHTML"], "lxml").find_all("li")
        # desc = [i.text.replace("\n\xa0\nNOA-RG", "").strip() for i in results if "Such as" not in i.text]
        # desc = None
        location = f"{data['JobPrimaryLocationCode']}, {data['JobLocationStateAbbrev']}".strip(
        )
        process_data.filter_jobs({
            "timestamp": post_date,
            "title": position,
            "company": company_name,
            "company_logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Nintendo.svg/600px-Nintendo.svg.png",
            "url": apply_url,
            "location": location,
            "source": company_name,
            "source_url": "https://careers.nintendo.com",
        })


def get_url():
    headers = {
        "User-Agent": random.choice(h.headers), "Origin": "https://careers.nintendo.com"}
    url = "https://2oc84v7py6.execute-api.us-west-2.amazonaws.com/prod/api/jobs/"
    response = requests.get(url, headers=headers)
    if response.ok:
        data = json.loads(response.text)
        get_results(data)
    else:
        print("=> nintendo: Error - Response status", response.status_code)


def main():
    get_url()


# main()
# sys.exit(0)
