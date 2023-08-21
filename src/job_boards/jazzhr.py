import requests
import sys
import time
import random
from datetime import datetime
from bs4 import BeautifulSoup
sys.path.insert(0, ".")
from src.job_boards.helpers import ProcessCompanyJobData, user_agents


process_data = ProcessCompanyJobData()
FILE_PATH = "src/data/params/jazzhr.txt"


def get_results(item: str, name: str):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all("li", class_="list-group-item")
    company = soup.find("meta", {"name": "twitter:title"})["content"].replace(
        " - Career Page", "") if soup.find("meta", {"name": "twitter:title"}) else None
    logo = soup.find(class_="").find("img")["src"] if soup.find(
        class_="").find("img", src=True) else None
    if results and company:
        for r in results:
            date = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
            post_date = datetime.timestamp(
                datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S"))
            apply_url = r.find("a")["href"].strip()
            company_name = company.strip()
            position = r.find("a").text.strip()
            location = r.find("ul").text.strip()
            process_data.filter_jobs({
                "timestamp": post_date,
                "title": position,
                "company": company_name,
                "company_logo": logo,
                "url": apply_url,
                "location": location,
                "source": company_name,
                "source_url": f"https://{name}.applytojob.com"
            })
    else:
        print(f"jazzhr => Error: check {company}")


def get_url(companies: list):
    page = 1
    for company in companies:
        try:
            headers = {"User-Agent": random.choice(user_agents)}
            url = f"https://{company}.applytojob.com"
            response = requests.get(url, headers=headers)
            if response.ok:
                get_results(response.text, company)
            elif response.status_code == 404:
                process_data.remove_not_found(FILE_PATH, company)
            else:
                f"=> jazzhr: Error for {company}. Status code: {response.status_code}"
            if page % 10 == 0:
                time.sleep(5)
            else:
                time.sleep(0.2)
            page += 1
        except Exception as e:
            print(f"=> jazzhr: Error for {company}. {e}")


def main():
    companies = process_data.read_list_of_companies(FILE_PATH)
    get_url(companies)


if __name__ == "__main__":
    main()