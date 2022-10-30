import requests
import json
import sys
import time
import random
from datetime import datetime
sys.path.insert(0, ".")
from server.job_boards.helpers.classes import ProcessCompanyJobData
from server.job_boards.helpers import headers as h
# import modules.headers as h

process_data = ProcessCompanyJobData()

def get_results(item: str):
    for i in item:
        job = i["node"]["data"]
        date = job["Created_Date"]
        post_date = datetime.timestamp(
            datetime.strptime(str(date), "%Y-%m-%dT%H:%M:%S.%fZ"))
        position = job["Role"].strip()
        company_name = job["Company"][0]["data"]["Name"].strip()
        logo = job["Company"][0]["data"]["Logo"][0]["thumbnails"]["large"]["url"]
        apply_url = "https://www.diversifytech.co/job-board/"+job["Job_ID"]
        location = job["Location"].strip()
        process_data.filter_jobs({
            "timestamp": post_date,
            "title": position,
            "company": company_name,
            "company_logo": logo,
            "url": apply_url,
            "location": location,
            "source": "Diversify Tech",
            "source_url": "https://www.diversifytech.co/"
        })


def get_url():
    try:
        headers = {"User-Agent": random.choice(h.headers)}
        url = "https://www.diversifytech.co/page-data/job-board/page-data.json"
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)[
            "result"]["data"]["allAirtable"]["edges"]
        if len(data) > 0:
            get_results(data)
        time.sleep(0.2)
    except Exception as e:
        print(f"=> diversifytech: Status code: {response.status_code}. Error: {e}..")


def main():
    get_url()

if __name__ == "__main__":
    main()
# sys.exit(0)
