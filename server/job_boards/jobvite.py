import requests
import sys
import time
import random
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from .modules import create_temp_json
from .modules import headers as h
from .modules import proxies as p
from .modules.classes import Read_List_Of_Companies, Remove_Not_Found
# import modules.create_temp_json as create_temp_json
# import modules.headers as h


FILE_PATH = "./data/params/jobvite.txt"


def get_jobs(date: str, apply_url: str, company_name: str, position: str, locations_string: str, logo: str, name: str):
    data = create_temp_json.data
    scraped = create_temp_json.scraped
    post_date = datetime.timestamp(datetime.strptime(str(date), "%Y-%m-%d"))
    data.append({
        "timestamp": post_date,
        "title": position,
        "company": company_name,
        "company_logo": logo,
        "url": apply_url,
        "location": locations_string,
        "source": company_name,
        "source_url": f"https://jobs.jobvite.com/careers/{name}",
        "category": "job"
    })
    scraped.add(company_name)
    print(f"=> jobvite: Added {position} for {company_name}")


def get_results(item: str, name: str):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all(
        class_="jv-job-list") if soup.find_all(class_="jv-job-list") else None
    company = soup.find("title").text.replace("Careers", "").replace(
        "| Available job openings", "").replace("Job listings |", "").strip() if soup.find("title") else None
    logo = soup.find(class_="logo")["src"] if soup.find(
        class_="logo", src=True) else None
    if results and company:
        for r in results:
            title = r.find(class_="jv-job-list-name").text.strip() if r.find(
                class_="jv-job-list-name") else r.find("a").text.strip()
            if "Engineer" in title or "Tech" in title or "Web" in title or "Data " in title or "QA" in title or "Cloud" in title or "IT " in title or "Software" in title or "Front" in title or "Back" in title:
                date = datetime.strftime(datetime.now(), "%Y-%m-%d")
                apply_url = "https://jobs.jobvite.com" + \
                    r.find("a")["href"].strip()
                company_name = company
                position = title
                locations_string = r.find("td", class_="jv-job-list-location").text.strip() if r.find(
                    "td", class_="jv-job-list-location") else "See description for location"
                get_jobs(date, apply_url, company_name,
                         position, locations_string, logo, name)


def get_url(companies: list):
    count = 1
    for name in companies:
        headers = {"User-Agent": random.choice(h.headers)}
        url = f"https://jobs.jobvite.com/careers/{name}"
        request = requests.Session()
        request.proxies.update(p.proxies)
        try:
            response = request.get(url, headers=headers)
            if response.ok:
                get_results(response.text, name)
            elif response.status_code == 404:
                Remove_Not_Found("./data/params/jobvite.txt", name)
                
            else:
                res = requests.get(
                    f"https://jobs.jobvite.com/{name}/jobs", headers=headers)
                if res.ok:
                    get_results(res.text, name)
                else:
                    print(
                        f"=> jobvite: Scrape failed for {name}. Status code: {res.status_code}")
        except:
            print("=> jobvite: Connection error:", name)
        if count % 20 == 0:
            time.sleep(5)
        count += 1


def main():
    companies = Read_List_Of_Companies(FILE_PATH)
    random.shuffle(companies)
    get_url(companies)


# main()
# sys.exit(0)
