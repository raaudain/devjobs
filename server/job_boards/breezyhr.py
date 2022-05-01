import requests
import sys
import time
import random
from datetime import datetime
from bs4 import BeautifulSoup
from .modules import create_temp_json
from .modules import headers as h
from .modules.classes import Create_Temp_JSON, List_Of_Companies, Page_Not_Found
# import modules.create_temp_json as create_temp_json
# import modules.headers as h
# import modules.classes as c


FILE_PATH = "./data/params/breezyhr.txt"


def get_jobs(date: str, url: str, company: str, position: str, location: str, logo: str, name: str):
    data = create_temp_json.data
    scraped = create_temp_json.scraped
    post_date = datetime.timestamp(
        datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S"))
    data.append({
        "timestamp": post_date,
        "title": position,
        "company": company,
        "company_logo": logo,
        "url": url,
        "location": location,
        "source": company,
        "source_url": f"https://{name}.breezy.hr",
        "category": "job"
    })
    scraped.add(company)
    print(f"=> breezyhr: Added {position} for {company}")


def get_results(item: str, name: str):
    soup = BeautifulSoup(item, "lxml")
    try:
        logo = None
        if soup.find(class_="brand").find("img"):
            logo = soup.find(class_="brand").find("img")["src"]
        results = soup.find_all("li", class_="position transition")
        company = soup.find("meta", {"name": "twitter:data1"})["content"] if soup.find(
            "meta", {"name": "twitter:data1"}) else name
        for r in results:
            h2 = r.find("h2").text
            if "Engineer" in h2 or "Data" in h2 or "IT " in h2 or "Support" in h2 or "Developer" in h2 or "QA " in h2 or "Engineer" in r.find("li", class_="department").text:
                date = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
                apply_url = f'https://{name}.breezy.hr{r.find("a")["href"].strip()}'
                company_name = company.strip()
                position = r.find("h2").text.strip()
                locations_string = "See description"

                if "%LABEL_POSITION_TYPE_REMOTE%" in r.find("li", class_="location").text:
                    locations_string = r.find("li", class_="location").text.replace(
                        "%LABEL_POSITION_TYPE_REMOTE%", "Remote")
                elif "%LABEL_POSITION_TYPE_WORLDWIDE%" in r.find("li", class_="location").text:
                    locations_string = r.find("li", class_="location").text.replace(
                        "%LABEL_POSITION_TYPE_WORLDWIDE%", "Remote")
                elif r.find("li", class_="location"):
                    locations_string = r.find(
                        "li", class_="location").text.strip()

                get_jobs(date, apply_url, company_name,
                         position, locations_string, logo, name)
    except AttributeError as err:
        print(f"=> breezyhr: Error for {name}.", err)


def get_url(companies: list):
    page = 1
    try:
        for company in companies:
            headers = {"User-Agent": random.choice(h.headers)}
            url = f"https://{company}.breezy.hr"
            response = requests.get(url, headers=headers)
            if response.ok:
                get_results(response.text, company)
                if page % 10 == 0:
                    time.sleep(5)
                page += 1
            elif response.status_code == 404:
                not_found = Page_Not_Found(FILE_PATH, company)
                not_found.remove_unwanted()
            elif str(response.status_code)[0] == "5":
                print(
                    f"=> breezyhr: Failed to scrape {company}. Status code: {response.status_code}")
                break
            else:
                print(
                    f"=> breezyhr: Failed to scrape {company}. Status code: {response.status_code}")
    except:
        print("=> breezyhr: Failed to scrape.")


def main():
    companies = List_Of_Companies(FILE_PATH).read_file()
    random.shuffle(companies)
    get_url(companies)


# main()
# sys.exit(0)
