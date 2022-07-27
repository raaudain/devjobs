from datetime import datetime
import requests
import json
import sys
import random
from .modules.classes import Filter_Jobs
from .modules import headers as h


def get_results(item: str):
    jobs = item["results"]
    for data in jobs:
        date = datetime.fromtimestamp(data["modified"] / 1e3)
        post_date = datetime.timestamp(
            datetime.strptime(str(date).rsplit(".")[0], "%Y-%m-%d %H:%M:%S"))
        apply_url = data["url"].strip()
        company_name = "Twitter"
        position = data["title"].strip()
        locations = ""
        for i in data["locations"]:
            locations += i["title"]+", "
        location = locations.rstrip(", ")
        Filter_Jobs({
            "timestamp": post_date,
            "title": position,
            "company": company_name,
            "company_logo": "https://logoeps.com/wp-content/uploads/2012/12/new-twitter-logo-vector.png",
            "url": apply_url,
            "location": location,
            "source": company_name,
            "source_url": "https://careers.twitter.com/"
        })


def get_url():
    headers = {"User-Agent": random.choice(h.headers)}
    url = "https://careers.twitter.com/content/careers-twitter/en/roles.careers.search.json?location=&team=careers-twitter:sr/team/it-it-enterprise-applications&team=careers-twitter:sr/team/data-science-and-analytics&team=careers-twitter:sr/team/customer-support-and-operations&team=careers-twitter:sr/team/software-engineering&team=careers-twitter:sr/team/infrastructure-engineering&team=careers-twitter:sr/team/security&team=careers-twitter:sr/team/product-and-design&team=careers-twitter:sr/team/machine-learning&offset=0&limit=1000&sortBy=modified&asc=false"
    response = requests.get(url, headers=headers)
    if response.ok:
        data = json.loads(response.text)
        get_results(data)
    else:
        print("=> twitter: Error - Response status", response.status_code)


def main():
    get_url()


# main()
# sys.exit(0)
