from datetime import datetime
from bs4 import BeautifulSoup
import requests, sys, time, random
from .modules import create_temp_json
from .modules import headers as h
# import modules.create_temp_json as create_temp_json
# import modules.headers as h


f = open(f"./data/params/breezyhr.txt", "r")
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
        "source_url": f"https://{name}.breezy.hr",
        "category": "job"
    })
    print(f"=> jazzhr: Added {title} for {company}")


def getResults(item, name):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all("li", class_="position transition")
    company = soup.find("meta", {"name":"twitter:data1"})["content"]

    for r in results:

        if "Engineer" in r.find("h2").text or "Data" in r.find("h2").text or "IT " in r.find("h2").text or "Support" in r.find("h2").text or "Developer" in r.find("h2").text or "QA " in r.find("h2").text or "Engineer" in r.find("li", class_="department").text:
            date = datetime.strftime(datetime.now(), "%Y-%m-%d")
            apply_url = f'https://{name}.breezy.hr{r.find("a")["href"].strip()}'
            company_name = company.strip()
            position = r.find("h2").text.strip()
            locations_string = r.find("li", class_="location").text.replace("%LABEL_POSITION_TYPE_REMOTE%", "Remote") if "%LABEL_POSITION_TYPE_REMOTE%" in r.find("li", class_="location").text else r.find("li", class_="location").text.strip()
            
            getJobs(date, apply_url, company_name, position, locations_string, name)
        

def getURL():
    page = 1

    for company in companies:
        try:
            headers = {"User-Agent": random.choice(h.headers)}
            url = f"https://{company}.breezy.hr"
            
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