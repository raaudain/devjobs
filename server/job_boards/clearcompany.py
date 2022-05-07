import requests
import sys
import time
import random
import json
from bs4 import BeautifulSoup
from datetime import datetime
from .modules.classes import Create_Temp_JSON, Filter_Jobs, Read_List_Of_Companies, Remove_Not_Found
from .modules import create_temp_json
from .modules import headers as h
# import modules.create_temp_json as create_temp_json
# import modules.headers as h
# import modules.classes as c


FILE_PATH = "./data/params/clearcompany.txt"


def get_jobs(date: str, url: str, company: str, position: str, location: str, param: str):
    data = create_temp_json.data
    scraped = create_temp_json.scraped
    post_date = datetime.timestamp(
        datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S"))
    data.append({
        "timestamp": post_date,
        "title": position,
        "company": company,
        "url": url,
        "location": location,
        "source": company,
        "source_url": f"https://{param}.hrmdirect.com/employment/job-openings.php?search=true&dept=-1",
        "category": "job"
    })
    scraped.add(company)
    print(f"=> clearcompany: Added {position} for {company}")


def get_results(item: str, param: str):
    soup = BeautifulSoup(item, "lxml")
    data = soup.find_all("tr", class_="reqitem ReqRowClick ReqRowClick")
    company = None
    if soup.find(class_="careersTitle"):
        company = soup.find(class_="careersTitle").text.replace(
            "Careers at", "").replace("Careers At", "").strip()
    elif soup.find(class_="footer-copyright"):
        company = soup.find(
            class_="footer-copyright").text.replace("© 2021", "").strip()
    else:
        company = param.upper()
    for d in data:
        title = d.find("td", class_="posTitle reqitem ReqRowClick").text
        # if "Engineer" in title or "Data" in title or "IT " in title or "Support" in title or "Cloud" in title or "Software" in title or "Developer" in title and ("Electrical" not in title and "HVAC" not in title and "Mechnical" not in title and "Data Entry" not in title and "Medication" not in title and "Environmental" not in title and "Nurse" not in title and "Manufactur" not in title and "Maintenance" not in title and "Health" not in title and "Civil" not in title):
        date = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
        post_date = datetime.timestamp(
            datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S"))
        apply_url = f"https://{param}.hrmdirect.com/employment/" + \
            d.find("a", href=True)["href"]
        company_name = company
        position = title.strip()
        city = d.find("a", href=True).find_next()
        state = city.find_next()
        location = f"{city.text.strip()}, {state.text.strip()}"
        Filter_Jobs({
            "timestamp": post_date,
            "title": position,
            "company": company_name,
            "url": apply_url,
            "location": location,
            "source": company_name,
            "source_url": f"https://{param}.hrmdirect.com/employment/job-openings.php?search=true&dept=-1"
        })


def get_url(companies: list):
    page = 1
    for company in companies:
        try:
            headers = {"User-Agent": random.choice(h.headers)}
            url = f"https://{company}.hrmdirect.com/employment/job-openings.php?search=true&dept=-1"
            response = requests.get(url, headers=headers)
            if response.ok:
                get_results(response.text, company)
                if page % 10 == 0:
                    time.sleep(5)
                page += 1
            elif response.status_code == 404:
                Remove_Not_Found(FILE_PATH, company)
            else:
                print(
                    f"=> clearcompany: Failed to scrape {company}. Status code: {response.status_code}")
        except:
            print(f"=> clearcompany: Error with {company}.")


def main():
    companies = Read_List_Of_Companies(FILE_PATH)
    get_url(companies)


# main()
# sys.exit(0)
