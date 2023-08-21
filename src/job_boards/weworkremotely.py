import requests
import sys
import random
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
sys.path.insert(0, ".")
from src.job_boards.helpers import CreateJson, user_agents, ProcessCompanyJobData


process_data = ProcessCompanyJobData()

def get_results(item: str):
    scraped = CreateJson.scraped
    try:
        soup = BeautifulSoup(item, "lxml")
        results = soup.find_all("li", class_=["feature", ""])
        for job in results:
            date = job.find("time")["datetime"].replace("T", " ").replace("Z", "") if job.find("time") else datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
            post_date = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))
            position = job.find("span", class_="title").text.strip()
            company_name = job.find("span", class_="company").text.strip()
            apply_url = "https://www.weworkremotely.com" + job.find_all("a", href=True)[1]["href"]
            location = job.find("span", class_="region company").contents[0].replace("Anywhere in the World", "Remote | Worldwide").replace("USA Only", "Remote | USA Only").replace("Europe Only", "Remote | Europe Only").replace(
                "Canada Only", "Remote | Canada Only").replace("North America Only", "Remote | North America Only").replace("Americas Only", "Remote | Americas Only") if job.find("span", class_="region company") else "Remote"
            logo = job.find(class_="flag-logo")["style"].replace("background-image:url(", "").replace("?ixlib=rails-4.0.0&w=50&h=50&dpr=2&fit=fill&auto=compress)", "") if job.find(class_="flag-logo") else None
            age = datetime.timestamp(datetime.now() - timedelta(days=30))

            if age <= post_date and company_name not in scraped:
                process_data.filter_jobs({
                    "timestamp": post_date,
                    "title": position,
                    "company": company_name,
                    "company_logo": logo,
                    "url": apply_url,
                    "location": location,
                    "source": "WeWorkRemotely",
                    "source_url": "https://weworkremotely.com/"
                })
    except Exception as e:
        print(f"=> weworkremotely: Error: {e}.")


def get_url():
    headers = {"User-Agent": random.choice(user_agents)}
    url = f"https://weworkremotely.com/remote-jobs/search?term=&button=&categories%5B%5D=2&categories%5B%5D=17&categories%5B%5D=18&categories%5B%5D=6"
    response = requests.get(url, headers=headers)
    if response.ok:
        get_results(response.text)
    else:
        print("=> weworkremotely: Error - Response status", response.status_code)


def main():
    get_url()


if __name__ == "__main__":
    main()
