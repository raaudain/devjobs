from datetime import datetime
from bs4 import BeautifulSoup
import requests, json, sys, time
from .modules import create_temp_json
# import modules.create_temp_json as create_temp_json


f = open(f"./data/params/jazzhr.txt", "r")
companies = [company.strip() for company in f]
f.close()

data = create_temp_json.data

def getJobs(date, url, company, position, location, name):
    date = str(date)
    title = position
    company = company
    url = url
    location = location

    # print(date, title, company, url, location)

    postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d"))
    
    data.append({
        "timestamp": postDate,
        "title": title,
        "company": company,
        "url": url,
        "location": location,
        "source": company,
        "source_url": f"https://{name}.applytojob.com",
        "category": "job"
    })
    print(f"=> jazzhr: Added {title} for {company}")


def getResults(item, name):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all("li", class_="list-group-item")
    company = soup.find("meta", {"name":"twitter:title"})["content"].replace(" - Career Page", "")

    for r in results:
        if "Engineer" in r.find("a").text or "Data" in r.find("a").text or "IT " in r.find("a") or "Support" in r.find("a").text:
            date = datetime.strftime(datetime.now(), "%Y-%m-%d")
            apply_url = r.find("a")["href"].strip()
            company_name = company.strip()
            position = r.find("a").text.strip()
            locations_string = r.find("ul").text.strip()
            
            getJobs(date, apply_url, company_name, position, locations_string, name)
        

def getURL():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"}

    page = 1

    for company in companies:
        try:
            url = f"https://{company}.applytojob.com"
            
            response = requests.get(url, headers=headers)

            if response.ok: getResults(response.text, company)

            if page % 10 == 0: time.sleep(5)
                    
            page+=1
        except:
            print(f"Failed to scrape {company}")
            continue
     

def main():
    getURL()

# main()
# sys.exit(0)