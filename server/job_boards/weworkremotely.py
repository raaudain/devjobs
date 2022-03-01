import requests, sys
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from .modules import create_temp_json
# import modules.create_temp_json as create_temp_json


def get_jobs(item: list):
    data = create_temp_json.data
    scraped = create_temp_json.scraped

    for job in item:
        date = job.find("time")["datetime"].replace("T", " ").replace("Z", "") if job.find("time") else datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
        title = job.find("span", class_="title").text.strip()
        company = job.find("span", class_="company").text.strip()
        url = "https://www.weworkremotely.com"+job.find_all("a", href=True)[1]["href"]
        location = job.find("span", class_="region company").contents[0].replace("Anywhere in the World", "Remote | Worldwide").replace("USA Only", "Remote | USA Only").replace("Europe Only", "Remote | Europe Only").replace("Canada Only", "Remote | Canada Only").replace("North America Only", "Remote | North America Only").replace("Americas Only", "Remote | Americas Only") if job.find("span", class_="region company") else "Remote"
        logo = job.find(class_="flag-logo")["style"].replace("background-image:url(", "").replace("?ixlib=rails-4.0.0&w=50&h=50&dpr=2&fit=fill&auto=compress)", "") if job.find(class_="flag-logo") else None

        age = datetime.timestamp(datetime.now() - timedelta(days=30))
        postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))

        if age <= postDate and company not in scraped:
            data.append({
                "timestamp": postDate,
                "title": title,
                "company": company,
                "company_logo": logo,
                "url": url,
                "location": location,
                "source": "WeWorkRemotely",
                "source_url": "https://weworkremotely.com/",
                "category": "job"
            })
            scraped.add(company)
        print(f"=> weworkremotely: Added {title} for {company}.")


def get_results(item: str):
    try:
        soup = BeautifulSoup(item, "lxml")
        results = soup.find_all("li", class_=["feature",""])
        get_jobs(results)
    except:
        print(f"=> weworkremotely: Error.")


def get_url():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"}
    url = f"https://weworkremotely.com/remote-jobs/search?term=&button=&categories%5B%5D=2&categories%5B%5D=17&categories%5B%5D=18&categories%5B%5D=6"
    response = requests.get(url, headers=headers)

    if response.ok: get_results(response.text)
    else: print("=> weworkremotely: Error - Response status", response.status_code)


def main():
    get_url()


# main()
# sys.exit(0)