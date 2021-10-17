import requests, json, sys, time, random
from datetime import datetime
from bs4 import BeautifulSoup
# from .modules import create_temp_json
# from .modules import headers as h
import modules.create_temp_json as create_temp_json
import modules.headers as h



def get_jobs(date: str, url: str, company: str, position: str, location: str, name: str):
    data = create_temp_json.data
    post_date = datetime.timestamp(datetime.strptime(str(date), "%Y-%m-%d"))
    
    data.append({
        "timestamp": post_date,
        "title": position,
        "company": company,
        "url": url,
        "location": location,
        "source": company,
        "source_url": f"https://{name}.applytojob.com",
        "category": "job"
    })
    print(f"=> jazzhr: Added {position} for {company}")


def get_results(item: str, name: str):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all("li", class_="list-group-item")
    company = soup.find("meta", {"name":"twitter:title"})["content"].replace(" - Career Page", "") if soup.find("meta", {"name":"twitter:title"}) else None

    if results and company:
        for r in results:
            if "Engineer" in r.find("a").text or "Data" in r.find("a").text or "IT " in r.find("a") or "Support" in r.find("a").text:
                date = datetime.strftime(datetime.now(), "%Y-%m-%d")
                apply_url = r.find("a")["href"].strip()
                company_name = company.strip()
                position = r.find("a").text.strip()
                locations_string = r.find("ul").text.strip()
                
                get_jobs(date, apply_url, company_name, position, locations_string, name)
    else:
        print(f"Check {company}")


def get_url(companies: list):
    page = 1

    for company in companies:
        # try:
        headers = {"User-Agent": random.choice(h.headers)}
        url = f"https://{company}.applytojob.com"
        response = requests.get(url, headers=headers)

        if response.ok: get_results(response.text, company)
        else: f"Error for {company}. Status code: {response.status_code}"

        if page % 10 == 0: time.sleep(5)
                
        page+=1


def main():
    f = open(f"./data/params/jazzhr.txt", "r")
    companies = [company.strip() for company in f]
    f.close()

    get_url(companies)


main()
sys.exit(0)