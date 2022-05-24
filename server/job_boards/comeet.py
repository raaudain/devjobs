import requests
import sys
import time
import random
import json
from bs4 import BeautifulSoup
from datetime import datetime
from .modules.classes import Filter_Jobs, Read_List_Of_Companies, Remove_Not_Found
from .modules import headers as h
# import modules.headers as h
# import modules.classes as c


FILE_PATH = "./data/params/comeet.txt"


def get_results(item: str, param: str):
    soup = BeautifulSoup(item, "lxml")
    logo = None
    results = soup.find("title").find_next(
        attrs={"type": "text/javascript"}).string
    r = results.split("COMPANY_POSITIONS_DATA = ",
                      1)[-1].rsplit("\n")[0].rstrip(";")
    l = results.split("COMPANY_DATA = ", 1)[-1].rsplit("\n")[0].rstrip(";")
    data = json.loads(r)
    img = json.loads(l)
    for k, v in img.items():
        if k == "logos":
            logo = v["original"]["url"]
    for d in data:
        if d["location"]:
            date = datetime.strptime(d["time_updated"], "%Y-%m-%dT%H:%M:%SZ")
            post_date = datetime.timestamp(
                datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S"))
            apply_url = d["url_active_page"]
            company_name = d["company_name"].strip()
            position = d["name"].strip()
            city = f"{d['location']['city'].strip()}, " if d["location"]["city"] else ""
            state = f"{d['location']['state'].strip()}, " if d["location"]["state"] else ""
            country = f"{d['location']['country'].strip()}" if d["location"]["country"] else ""
            location = f"{city}{state}{country} | Remote" if d["location"][
                "is_remote"] == True else f"{city}{state}{country}"
            Filter_Jobs({
                "timestamp": post_date,
                "title": position,
                "company": company_name,
                "company_logo": logo,
                "url": apply_url,
                "location": location,
                "source": company_name,
                "source_url": f"https://www.comeet.com/jobs/{param}"
            })


def get_url(companies: list):
    page = 1
    for company in companies:
        try:
            headers = {"User-Agent": random.choice(h.headers)}
            url = f"https://www.comeet.com/jobs/{company}"
            response = requests.get(url, headers=headers)
            if response.ok:
                get_results(response.text, company)
                if page % 10 == 0:
                    time.sleep(5)
                else:
                    time.sleep(0.2)
                page += 1
            elif response.status_code == 404:
                Remove_Not_Found(FILE_PATH, company)
            else:
                print(
                    f"=> comeet: Failed to scrape {company}. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error for {company}. {e}")


def main():
    companies = Read_List_Of_Companies(FILE_PATH)
    get_url(companies)


# main()
# sys.exit(0)
