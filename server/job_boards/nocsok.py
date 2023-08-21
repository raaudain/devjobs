from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests
import random
import sys
sys.path.insert(0, ".")
from server.job_boards.helpers import headers as h
from server.job_boards.helpers.classes import ProcessCompanyJobData


def get_results(item: str):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all("div", class_="w-100 jobboard-card-child")
    process_data = ProcessCompanyJobData()

    for job in results:
        date = datetime.strptime(job.find_all(
            "small")[1].text+" 2022", "%b %d %Y")
        title = job.find("strong").text
        company_name = job.find("small").text
        apply_url = "https://nocsok.com/" + \
            job.find("a", href=True)["href"].replace("#", "")
        location = job.find("h5").text.strip()
        age = datetime.timestamp(datetime.now() - timedelta(days=30))
        post_date = datetime.timestamp(
            datetime.strptime(str(date)[:-9], "%Y-%m-%d "))
    
        if age <= post_date:
            process_data.filter_jobs({
                "timestamp": post_date,
                "title": title,
                "company": company_name,
                "company_logo": "https://i.ibb.co/ygrqSj8/No-CSDegree-logo.jpg",
                "url": apply_url,
                "location": location,
                "source": "NoCSOK",
                "source_url": "https://nocsok.com/",
                "category": "job"
            })


def get_url():
    headers = {"User-Agent": random.choice(h.headers)}
    url = "https://www.nocsdegree.com/jobs/"
    response = requests.get(url, headers=headers)

    if response.ok:
        get_results(response.text)
    else:
        print("=> nocsok: Error - Response status", response.status_code)


def main():
    get_url()


if __name__ == "__main__":
    main()
    sys.exit(0)
