from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests, json, sys, time
from .modules import create_temp_json
# import modules.create_temp_json as create_temp_json


data = create_temp_json.data
f = open(f"./data/params/greenhouse_io.txt", "r")
companies = [company.strip() for company in f]
f.close()

def getJobs(date, url, company, position, location, name, qualifications):
    date = str(date)
    title = position
    qualifications = qualifications
    company = company
    url = url
    location = location

    # age = datetime.timestamp(datetime.now() - timedelta(days=7))
    postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d %H:%M:%S%z"))
    
    data.append({
        "timestamp": postDate,
        "title": title,
        "qualifications": qualifications,
        "company": company,
        "url": url,
        "location": location,
        "source": company,
        "source_url": f"https://boards.greenhouse.io/{name}",
        "category": "job"
    })
    print(f"=> greenhouse.io: Added {title} for {company}")
            


def getResults(item, name, company):
    data = item["departments"]
    jobs = []

    for d in data:
        if "Engineer" in d["name"] or "Tech" in d["name"] or "Data" in d["name"] or "Software" in d["name"] or "IT" in d["name"] or "Information" in d["name"] or "Development" in d["name"] or "Programming" in d["name"] or "Quality Assurance" in d["name"] or "QA" in d["name"] and (["Music"] not in d["name"] or ["Art"] not in d["name"] or ["Talent"] not in d["name"] or "Business" not in d["name"]):
            if d["jobs"]:
                jobs.extend(d["jobs"])

    for j in jobs:
        # if "Engineer" in j["title"] or "Data" in j["title"] or "Support" in d["title"] or "IT" in d["title"] or "Programmer" in d["title"] or "QA" in d["title"] or "Software" in d["title"]  or "Tech " in d["title"]:
        jobId = j["id"]
        content = json.loads(requests.get(f"https://boards-api.greenhouse.io/v1/boards/{name}/jobs/{jobId}").text)["content"].replace("&lt;", "<").replace("&gt;", ">")
        soup = BeautifulSoup(content, "lxml")
        results = soup.find_all("ul")[1].find_all_next("li")
        desc = [r.text.replace("&nbsp;", " ").replace("&amp;", "&").strip() for r in results]
        # print(desc)

        date = datetime.strptime(j["updated_at"], "%Y-%m-%dT%H:%M:%S%z")
        position = j["title"].strip()
        company_name = company
        apply_url = j["absolute_url"].strip()
        locations_string = j["location"]["name"].strip()

        getJobs(date, apply_url, company_name, position, locations_string, name, desc)


def getURL():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"}

    count = 1

    for name in companies:
        try:
            url = f"https://boards-api.greenhouse.io/v1/boards/{name}/departments"
            url2 = f"https://boards-api.greenhouse.io/v1/boards/{name}/"

            response = requests.get(url, headers=headers).text
            res = requests.get(url2, headers=headers).text

            data = json.loads(response)
            company = json.loads(res)["name"]

            getResults(data, name, company)
            
            if count % 10 == 0:
                time.sleep(5)
                
            count+=1
        except:
            print(f"Failed to scraped: {name}")
            continue
     


def main():
    getURL()

# main()
# sys.exit(0)