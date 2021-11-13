import requests, sys, time, random
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from .modules import create_temp_json
from .modules import headers as h
# import modules.create_temp_json as create_temp_json
# import modules.headers as h


def get_jobs(date: str, apply_url: str, company_name: str, position: str, locations_string: str, name: str):
    data = create_temp_json.data
    scraped = create_temp_json.scraped
    post_date = datetime.timestamp(datetime.strptime(str(date), "%Y-%m-%d"))

    data.append({
        "timestamp": post_date,
        "title": position,
        "company": company_name,
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
    results = soup.find_all(class_="jv-job-list")
    company = soup.find("title").text.replace("Careers", "").replace("| Available job openings", "").replace("Job listings |", "").strip()
    
    if results and company:
        for r in results:
            try:
                title = r.find(class_="jv-job-list-name").text.strip()

                if "Engineer" in title or "Tech" in title or "Web" in title or "Data " in title or "QA" in title or "Cloud" in title or "IT " in title or "Software" in "title" or "Front" in title or "Back" in title:
                    date = datetime.strftime(datetime.now(), "%Y-%m-%d")
                    apply_url = "https://jobs.jobvite.com"+r.find("a")["href"].strip()
                    company_name = company
                    position = title
                    locations_string = r.find("td", class_="jv-job-list-location").text.strip()
                    
                    get_jobs(date, apply_url, company_name, position, locations_string, name)
            except AttributeError:
                print(f"=> jobvite: Failed: {company}")
                pass


def get_url(companies: list):
    count = 1

    for name in companies:
        headers = {"User-Agent": random.choice(h.headers)}
        url = f"https://jobs.jobvite.com/careers/{name}"
        response = requests.get(url, headers=headers)

        if response.ok: get_results(response.text, name)
        else: 
            res = requests.get(f"https://jobs.jobvite.com/{name}", headers=headers)

            if res.ok: get_results(res.text, name)
            else: print(f"=> jobvite: Scrape failed for {name}. Status code: {res.status_code}")

        if count % 10 == 0: time.sleep(5)
        count+=1


def main():
    f = open(f"./data/params/jobvite.txt", "r")
    companies = [company.strip() for company in f]
    f.close()

    get_url(companies)


# main()
# sys.exit(0)