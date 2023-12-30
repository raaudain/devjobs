import sys
import random
from datetime import datetime
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
sys.path.insert(0, ".")
from src.job_boards.helpers import ProcessCompanyJobData, user_agents


process_data = ProcessCompanyJobData()
FILE_PATH = "src/data/params/lever_co.txt"

def get_results(page, param):
    soup = BeautifulSoup(page, "lxml")
    main_header = soup.find(class_="main-header-logo")
    logo = main_header.find("img").get("src") if main_header else None
    company_name = soup.find("title").text if "error" not in soup.find("title") else param.capitalize()
    source_url = f"https://jobs.lever.co/{param}"
    date = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
    post_date = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))

    for posting in soup.find_all(class_="posting"):
        workplace_type = f"{posting.find(class_='workplaceTypes').text} - " if posting.find(class_="workplaceTypes") else ""
        physical_location = posting.find(class_='sort-by-location').text if posting.find(class_="sort-by-location") else ""
        location = workplace_type.replace('\xa0—\xa0', '') + physical_location

        process_data.filter_jobs({
            "timestamp":post_date,
            "title": posting.find(attrs={"data-qa": "posting-name"}).text,
            "company": company_name,
            "company_logo": logo,
            #"description": description,
            "url": posting.find(class_="posting-title").get("href"),
            "location": location,
            "source": company_name,
            "source_url": source_url
        })

def get_url(companies):
    for company in companies:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(user_agent=f"{random.choice(user_agents)}")
            page.goto(f"https://jobs.lever.co/{company}")
            content = page.content()
            get_results(content, company)
            browser.close()

def main():
    companies = process_data.read_list_of_companies(FILE_PATH)
    get_url(companies)

if __name__ == "__main__":
    main()