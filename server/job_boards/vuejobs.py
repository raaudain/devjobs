import requests
import json
import sys
import time
import random
from datetime import datetime, timedelta
sys.path.insert(0, ".")
from server.job_boards.helpers import headers as h
from server.job_boards.helpers.classes import ProcessCompanyJobData
# import modules.headers as h



def get_results(item: str):
    process_data = ProcessCompanyJobData()

    for i in item["data"]:
        date = i["published_at"].rsplit("+")[0]
        post_date = int(datetime.timestamp(
            datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")))
        apply_url = i["link"]
        company_name = i["organization"]["name"]
        logo = i["organization"]["avatar"]
        position = i["title"]
        description = i["description"]
        location = [location for location in i["locations"] if len(location) > 0 else None]
        age = datetime.timestamp(datetime.now() - timedelta(days=30))
        if age <= post_date:
            process_data.filter_jobs({
                "timestamp": post_date,
                "title": position,
                "company": company_name,
                "company_logo": logo,
                #"description": description,
                "url": apply_url,
                "location": location,
                "source": "VueJobs",
                "source_url": "https://vuejobs.com/"
            })


def get_url():
    headers = {"User-Agent": random.choice(h.headers)}
    url = f"https://app.vuejobs.com/posts/items"
    response = requests.get(url, headers=headers)

    if response.ok:
        data = json.loads(response.text)
        get_results(data)
    else:
        print("=> vuejobs: Failed. Status code:", response.status_code)


def main():
    get_url()


if __name__ == "__main__":
    main()
    sys.exit(0)
