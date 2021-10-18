import requests, sys, time, random
from bs4 import BeautifulSoup
from datetime import datetime
from .modules import create_temp_json
from .modules import headers as h
# import modules.create_temp_json as create_temp_json
# import modules.headers as h


def get_jobs(item: list, company: str, source_url: str):
    data = create_temp_json.data
    scraped = create_temp_json.scraped

    for job in item:
        # try:
        date = datetime.strftime(datetime.now(), "%Y-%m-%d")
        title = job.find("h5", {"data-qa": "posting-name"}).text
        company = company
        url = job["href"]
        location = job.find("span", {"class": "sort-by-location posting-category small-category-label"}).text

        post_date = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d"))

        if url not in scraped:
            data.append({
                "timestamp": post_date,
                "title": title,
                "company": company,
                "url": url,
                "location": location,
                "source": company,
                "source_url": source_url,
                "category": "job"
            })
            scraped.add(url)
            scraped.add(company)
            print(f"=> lever.co: Added {title} for {company}")
        else:
            print(f"=> lever.co: Already scraped {title} for {company}")
        # except:
        #     print(f"=> lever.co: Scrape failed for {title} - {company}. Going to next.")
        #     continue

def get_results(item: str, name: str):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all("a", {"class": "posting-title"})
    company = soup.find("title").text.strip()
    source_url = f"https://jobs.lever.co/{name}"

    postings = []

    for result in results:
        h5 = result.find("h5", {"data-qa":"posting-name"}).text
        if ("Engineer" in h5 or "Tech" in h5 or "Web" in h5 or "Data " in h5) and ("Pharmacy Tech" not in h5 or "Pharmacy Clerk" not in h5):
            postings.append(result)

    results = postings

    get_jobs(results, company, source_url)


def get_url(companies: list):
    count = 1

    for name in companies:
        headers = {"User-Agent": random.choice(h.headers)}
        url = f"https://jobs.lever.co/{name}"
        response = requests.get(url, headers=headers)

        if response.ok: get_results(response.text, name)
        else: print(f"=> lever.co: Error for {name} - Response status", response.status_code)
        
        if count % 20 == 0: time.sleep(5)
            
        count+=1
        

def main():
    f = open("./data/params/lever_co.txt", "r")
    companies = [company.strip() for company in f]
    f.close()

    get_url(companies)


# main()
# sys.exit(0)