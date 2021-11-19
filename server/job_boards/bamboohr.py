import requests, sys, time, random, json
from bs4 import BeautifulSoup
from datetime import datetime
from .modules import create_temp_json
from .modules import headers as h
# import modules.create_temp_json as create_temp_json
# import modules.headers as h


def get_jobs(date: str, url: str, company: str, position: str, location: str, param: str):
    data = create_temp_json.data
    scraped = create_temp_json.scraped

    post_date = datetime.timestamp(datetime.strptime(str(date), "%Y-%m-%d"))
    
    data.append({
        "timestamp": post_date,
        "title": position,
        "company": company,
        "url": url,
        "location": location,
        "source": company,
        "source_url": f"https://{param}.bamboohr.com/jobs/",
        "category": "job"
    })
    scraped.add(company)
    print(f"=> bamboohr: Added {position} for {company}")


def get_results(item: str, param: str):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find(attrs={"type": "json"}).string
    data = json.loads(results)
    company = soup.find("img")["alt"]

    for d in data:
        if "Engineer" in d["jobOpeningName"] or "Data" in d["jobOpeningName"] or "Data" in d["jobOpeningName"] or "IT " in d["jobOpeningName"] or "Tech" in d["jobOpeningName"] or "Support" in d["jobOpeningName"] or "Cloud" in d["jobOpeningName"] or "Software" in d["jobOpeningName"] or "Developer" in d["jobOpeningName"] and ("Electrical" not in d["jobOpeningName"] and "HVAC" not in d["jobOpeningName"] and "Mechnical" not in d["jobOpeningName"]):
            date = datetime.strftime(datetime.now(), "%Y-%m-%d")
            apply_url = f"https://{param}.bamboohr.com/jobs/view.php?id={d['id']}"
            company_name = company.strip()
            position = d["jobOpeningName"].strip()
            locations_string = f"{d['location']['city'].strip()}, {d['location']['state'].strip() if d['location']['state'] else d['location']['country'].strip()}"
            
            get_jobs(date, apply_url, company_name, position, locations_string, param)


def get_url(companies: list):
    page = 1

    for company in companies:
        headers = {"User-Agent": random.choice(h.headers)}
        url = f"https://{company}.bamboohr.com/jobs/"
        response = requests.post(url, headers=headers)

        if response.ok:
            get_results(response.text, company)
            if page % 10 == 0: time.sleep(5)   
            page+=1
        else:
            print(f"=> bamboohr: Failed to scrape {company}. Status code: {response.status_code}")


def main():
    f = open(f"./data/params/bamboohr.txt", "r")
    companies = [company.strip() for company in f]
    f.close()

    get_url(companies)


# main()
# sys.exit(0)