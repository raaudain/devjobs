import requests
import sys
import time
import random
from bs4 import BeautifulSoup
from datetime import datetime
sys.path.insert(0, ".")
from src.job_boards.helpers import ProcessCompanyJobData, user_agents


process_data = ProcessCompanyJobData()
FILE_PATH = "src/data/params/key_values.txt"


def get_results(item: str, url: str):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all("div", class_="open-position-item-contents")
    logo = soup.find(class_="hero-logo")["style"].replace("background: url(", "").replace(
        ") no-repeat center center; background-size: contain;", "") if soup.find(class_="hero-logo") else None
    for job in results:
        date = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
        post_date = datetime.timestamp(
            datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))
        title = job.find("p", class_="open-position--job-title").text
        company = job.find("a")["data-company"]
        apply_url = job.find("a", href=True)["href"]
        location = job.find(
            "div", class_="open-position--job-information").find_all("p")[0].text
        process_data.filter_jobs({
            "timestamp": post_date,
            "title": title,
            "company": company,
            "company_logo": logo,
            "url": apply_url,
            "location": location,
            "source": "Key Values",
            "source_url": url,
        })


def get_url(params: list):
    for param in params:
        headers = {"User-Agent": random.choice(user_agents)}
        url = f"https://www.keyvalues.com{param}"
        response = requests.get(url, headers=headers)
        if response.ok:
            get_results(response.text, url)
        else:
            print(f"=> key_values: Error. Status code:", response.status_code)
        time.sleep(2)


def main():
    process_data.filter_key_values_companies()
    params = process_data.read_list_of_companies(FILE_PATH)
    get_url(params)


if __name__ == "__main__":
    main()
