import requests
import json
import sys
import time
import random
from datetime import datetime
from .helpers import headers as h
from .helpers.classes import Filter_Jobs


def getResults(item):
    jobs = item["Jobs"]
    for data in jobs:
        date = datetime.strptime(data["DateDisplay"][:13][5:], "%m/%d/%y")
        post_date = datetime.timestamp(
            datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S"))
        apply_url = data["PositionURI"]
        company_name = data["Agency"].strip()
        position = data["Title"].strip()
        location = data["Location"].strip()
        Filter_Jobs({
            "timestamp": post_date,
            "title": position,
            "company": company_name,
            "company_logo": "https://careersourcefloridacrown.com/wp-content/uploads/2017/06/usajobs.png",
            "url": apply_url,
            "location": location,
            "source": "USAJobs",
            "source_url": "https://www.usajobs.gov/"
        })


def getURL():
    headers = {"User-Agent": random.choice(h.headers)}
    page = 1
    while page < 50:
        try:
            url = "https://www.usajobs.gov/Search/ExecuteSearch"
            payload = {
                "HiringPath": ["public"],
                "Page": page,
                "Keyword": "software",
                "UniqueSearchID": "162dbbf5-6795-4786-840e-efd686188e29",
                "IsAuthenticated": False
            }
            response = requests.post(url, json=payload, headers=headers).text
            data = json.loads(response)
            getResults(data)
            if page % 5 == 0:
                time.sleep(5)
            else:
                time.sleep(0.2)
            page += 1
        except Exception as e:
            print(f"=> usajobs: Failed to scrap page {page}. Error: {e}.")
            break


def main():
    getURL()


# if __name__ == "__main__":
#     main()
