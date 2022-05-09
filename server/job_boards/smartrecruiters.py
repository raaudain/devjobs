from datetime import datetime
from lxml import html
import requests
import sys
import json
import time
import random
from .modules import headers as h
from .modules.classes import Filter_Jobs, Read_List_Of_Companies, Remove_Not_Found
# import modules.headers as h
# import modules.classes as c


FILE_PATH = "./data/params/smartrecruiters.txt"


def get_results(item: str, name: str):
    data = item["content"]
    images = {}
    if data:
        for i in data:
            date = datetime.strptime(
                i["releasedDate"], "%Y-%m-%dT%H:%M:%S.%fZ")
            post_date = datetime.timestamp(
                datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S"))
            jobId = i["id"]
            company_name = i["company"]["name"]
            apply_url = f"https://jobs.smartrecruiters.com/{name}/{jobId}"
            logo = None
            # if name in images:
            #     logo = images[name]
            # else:
            #     r = requests.get(apply_url)
            #     if r.ok:
            #         tree = html.fromstring(r.content)
            #         img = tree.xpath(
            #             "//*[@class='header-logo logo']")
            #         if img:
            #             image = tree.xpath("//*[@class='header-logo logo']//img/@src")
            #             logo = image
            #             images[name] = logo
            position = i["name"]
            city = f'{i["location"]["city"]}, '
            region = f'{i["location"]["region"]}, ' if "region" in i["location"] else ""
            country = i["location"]["country"].upper()
            remote = " | Remote" if i["location"]["remote"] else ""
            location = f"{city}{region}{country}{remote}"
            Filter_Jobs({
                "timestamp": post_date,
                "title": position,
                "company": company_name,
                "company_logo": logo,
                "url": apply_url,
                "location": location,
                "source": company_name,
                "source_url": f"https://careers.smartrecruiters.com/{name}/",
                "category": "job"
            })
    else:
        print(f"=> smartrecruiters: No jobs for {name}.")


def get_url(companies: list):
    count = 1
    for name in companies:
        try:
            headers = {"User-Agent": random.choice(h.headers)}
            url = f"https://api.smartrecruiters.com/v1/companies/{name}/postings/"
            response = requests.get(url, headers=headers)
            print(response.ok)
            if response.ok:
                data = json.loads(response.text)
                get_results(data, name)
                if count % 20 == 0:
                    time.sleep(5)
                count += 1
            elif response.status_code == 404:
                Remove_Not_Found(FILE_PATH, name)
        except:
            if response.status_code == 429:
                print(
                    f"=> smartrecruiters: Failed to scraped {name}. Status code: {response.status_code}.")
                break
            else:
                print(
                    f"=> smartrecruiters: Failed to scraped {name}. Status code: {response.status_code}.")


def main():
    companies = Read_List_Of_Companies(FILE_PATH)
    get_url(companies)


# main()
# sys.exit(0)
