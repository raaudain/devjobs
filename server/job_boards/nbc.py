import requests
import json
import sys
import time
import random
from datetime import datetime
from .helpers import create_temp_json
from .helpers import headers as h
from .helpers.classes import Filter_Jobs
# import modules.create_temp_json as create_temp_json
# import modules.headers as h


def get_results(item: str):
    for i in item:
        date = i["field_lastupdated"]+"/2021"
        post_date = datetime.timestamp(
            datetime.strptime(str(date), "%m/%d/%Y"))
        position = i["title"].strip()
        company_name = "NBCUniversal"
        apply_url = i["field_detailurl"].replace("&amp;", "&").strip()
        location = ",".join(i["field_location"].split(",")[::-1]).replace(",United States", "").strip() if len(
            i["field_location"].split(",")) < 4 else i["field_location"].replace("United States,", "").strip()
        Filter_Jobs({
            "timestamp": post_date,
            "title": position,
            "company": company_name,
            "company_logo": "https://www.complaintsboard.com/img/business/121585/200x200/nbcuniversal.jpg",
            "url": apply_url,
            "location": location,
            "source": company_name,
            "source_url": "https://www.nbcunicareers.com/careers",
        })


def get_url():
    page = 0
    items = 10
    while items > 0:
        headers = {"User-Agent": random.choice(h.headers)}
        url = f"https://www.nbcunicareers.com/api/brjobs?_format=json&page={page}&profession=1098"
        response = requests.get(url, headers=headers)
        if response.ok:
            data = json.loads(response.text)[0]["rows"]
            get_results(data)
        else:
            print(f"Error. Status Code:", response.status_code)
        page += 1
        items = len(data)
        time.sleep(0.2)


def main():
    get_url()


# main()
# sys.exit(0)
