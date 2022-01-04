from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests, sys
from .modules import create_temp_json


def get_jobs(item: list):
    data = create_temp_json.data

    for job in item:
        date = datetime.strptime(job.find_all("small")[1].text+" 2021", "%b %d %Y")
        title = job.find("strong").text
        company = job.find("small").text
        url = "https://nocsok.com/"+job.find("a", href=True)["href"].replace("#", "")
        location = job.find("h5").text.strip()

        age = datetime.timestamp(datetime.now() - timedelta(days=30))
        postDate = datetime.timestamp(datetime.strptime(str(date)[:-9], "%Y-%m-%d"))

        if age <= postDate:
            data.append({
                "timestamp": postDate,
                "title": title,
                "company": company,
                "company_logo": "https://i.ibb.co/ygrqSj8/No-CSDegree-logo.jpg",
                "url": url,
                "location": location,
                "source": "NoCSOK",
                "source_url": "https://nocsok.com/",
                "category": "job"
            })
            print(f"=> nocsok: Added {title}")


def get_results(item: str):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all("div", {"class": "w-100 jobboard-card-child"})
    # print(results)
    get_jobs(results)


def get_url():
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}
    url = f"https://nocsok.com/"
    response = requests.get(url, headers=headers)

    if response.ok: get_results(response.text)
    else: print("=> nocsok: Error - Response status", response.status_code)
    # print(response)

def main():
    get_url()
