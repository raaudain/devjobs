import requests, json, sys, time, random
from datetime import datetime
from bs4 import BeautifulSoup
# from .modules import create_temp_json
# from .modules import headers as h
import modules.create_temp_json as create_temp_json
import modules.headers as h


def get_jobs(date: str, url: str, company: str, position: str, location: str):
    data = create_temp_json.data
    post_date = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d"))
    
    data.append({
        "timestamp": post_date,
        "title": position,
        # "qualifications": qualifications,
        "company": company,
        "url": url,
        "location": location,
        "source": "Bloomberg",
        "source_url": "https://www.bloomberg.com/company/what-we-do/",
        "category": "job"
    })
    print(f"=> bloomberg: Added {position} for {company}")


def get_results(item):
    print(item)
    date = item["datePosted"]
    apply_url = item["url"]
    company_name = "Bloomberg"
    position = item["jobTitle"]
    locations_string = item["jobLocation"]
    # soup = BeautifulSoup(item["jobDescription"], "lxml")
    # results = soup.find_all("ul")[-1].find_all_next("li")
    # desc = []

    # for i in results: desc.append(i.text.strip())
    get_jobs(date, apply_url, company_name, position, locations_string)


def get_url():
    # session = requests.Session()
    # cookie = session.get("https://careers.bloomberg.com/job/search?&amp;_ga=2.132473930.596821302.1561381910-831768493.1559310775").cookies.get_dict()
    # print(cookie)
    headers = {"User-Agent": random.choice(h.headers), "X-Requested-With": "XMLHttpRequest", "Cookie":"l=jfEMhxe6KxjiGjtNRhEjrw.ar-sH2mKPUK-8sPEFAlbsTFcEOhm9N70RygL5ySOGM4skK3s3lXBiGFlBEV8oJGR18K8E4yKEyWkIz3uJVc25w.1635229659446.3600000.4hucrhjxXi9Uqjz6UZWBCPGDgKQYxnACY7IEwQkfXDI"}
    # headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36", "X-Requested-With": "XMLHttpRequest"}
    url_1 = f"https://careers.bloomberg.com/job_search/search_query?autocompleteTags=%5B%5D&selectedFilterFields=%5B%7B%22name%22%3A%22Software+Developer%2FEngineering%22%2C%22count%22%3A%22239%22%2C%22isSelected%22%3Atrue%2C%22parentFacet%22%3A%22Job+function%22%2C%22id%22%3A%22c41%22%7D%2C%7B%22name%22%3A%22Technical+Support%22%2C%22count%22%3A%2216%22%2C%22isSelected%22%3Atrue%2C%22parentFacet%22%3A%22Job+function%22%2C%22id%22%3A%22c48%22%7D%5D&jobStartIndex=0&jobBatchSize=1000"
    response = requests.get(url_1, headers=headers).text
    data = json.loads(response)
    job_id = []

    for d in data["jobData"]:
        if "engineer" in d["Specialty"]["Value"].lower() or "tech" in d["Specialty"]["Value"].lower(): job_id.append(d["JobReqNbr"])
    
    count = 1

    for j in job_id:
        url_2 = f"https://careers.bloomberg.com/job_search/detail_query?job_id={j}"
        res = requests.get(url_2, headers=headers)

        if res.ok:
            post = json.loads(res.text)
            # get_results(post)
            print("hey",post)
            if count % 10 == 0: time.sleep(5)
            count+=1
        else:
            print(f"bloomberg: Failed for ID {j}. Status code: {res.status_code}.")


def main():
    get_url()

main()
sys.exit(0)

