import requests, sys, time, random, json, re
from bs4 import BeautifulSoup
from datetime import datetime
from .modules.classes import Create_Temp_JSON, Page_Not_Found
from .modules import create_temp_json
from .modules import headers as h
# import modules.create_temp_json as create_temp_json
# import modules.headers as h
# import modules.classes as c


def get_jobs(date: str, url: str, company: str, position: str, location: str, param: str):
    data = create_temp_json.data
    scraped = create_temp_json.scraped

    # data = Create_Temp_JSON.data
    # scraped = Create_Temp_JSON.scraped

    post_date = datetime.timestamp(datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S"))
    
    data.append({
        "timestamp": post_date,
        "title": position,
        "company": company,
        "url": url,
        "location": location,
        "source": company,
        "source_url": f"https://www.comeet.com/jobs/{param}",
        "category": "job"
    })
    scraped.add(company)
    print(f"=> comeet: Added {position} for {company}")


def get_results(item: str, param: str):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find(attrs={"type": "text/javascript"}).string
    r = results.split("COMPANY_POSITIONS_DATA = ", 1)[-1].rsplit("\n")[0].rstrip(";")
    data = json.loads(r)

    for d in data:
        if "Engineer" in d["name"] or "Data" in d["name"] or "Data" in d["name"] or "IT " in d["name"] or "Tech" in d["name"] or "Support" in d["name"] or "Cloud" in d["name"] or "Software" in d["name"] or "Developer" in d["name"] and ("Electrical" not in d["name"] and "HVAC" not in d["name"] and "Mechnical" not in d["name"] and "Hardware" not in d["name"]):
            date = datetime.strptime(d["time_updated"], "%Y-%m-%dT%H:%M:%SZ")
            apply_url = d["url_active_page"]
            company_name = d["company_name"].strip()
            position = d["name"].strip()
            city = f"{d['location']['city'].strip()}, " if d["location"]["city"] else ""
            state = f"{d['location']['state'].strip()}, " if d["location"]["state"] else ""
            country = f"{d['location']['country'].strip()}" if d["location"]["country"] else ""
            locations_string = f"{city}{state}{country} | Remote" if d["location"]["is_remote"] == True else f"{city}{state}{country}"
            
            get_jobs(date, apply_url, company_name, position, locations_string, param)


def get_url(companies: list):
    page = 1

    for company in companies:
        headers = {"User-Agent": random.choice(h.headers)}
        url = f"https://www.comeet.com/jobs/{company}"
        response = requests.get(url, headers=headers)

        if response.ok:
            get_results(response.text, company)
            if page % 10 == 0: time.sleep(5)   
            page+=1
        elif response.status_code == 404:
            not_found = Page_Not_Found("./data/params/comeet.txt", company)
            not_found.remove_unwanted()
        else:
            print(f"=> comeet: Failed to scrape {company}. Status code: {response.status_code}")


def main():
    f = open(f"./data/params/comeet.txt", "r")
    companies = [company.strip() for company in f]
    f.close()

    get_url(companies)


# main()
# sys.exit(0)