import requests, json, sys, time, random
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from .modules import create_temp_json
from .modules import headers as h
# import modules.create_temp_json as create_temp_json
# import modules.headers as h


def get_jobs(date: str, url: str, company: str, position: str, location: str, name: str):
    data = create_temp_json.data
    scraped = create_temp_json.scraped

    post_date = datetime.timestamp(datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S%z"))
    
    data.append({
        "timestamp": post_date,
        "title": position,
        # "qualifications": qualifications,
        "company": company,
        "url": url,
        "location": location,
        "source": company,
        "source_url": f"https://boards.greenhouse.io/{name}",
        "category": "job"
    })
    scraped.add(company)
    print(f"=> greenhouse.io: Added {position} for {company}")
            
def get_results(item: str, name: str, company: str):
    # data = item["departments"]
    jobs = item["jobs"]

    # for d in data:
    #     if "Engineer" in d["name"] or "Tech" in d["name"] or "Data" in d["name"] or "Software" in d["name"] or "IT" in d["name"] or "Information" in d["name"] or "Development" in d["name"] or "Programming" in d["name"] or "Quality Assurance" in d["name"] or "QA" in d["name"] and (["Music"] not in d["name"] or ["Art"] not in d["name"] or ["Talent"] not in d["name"] or "Business" not in d["name"]):
    #         if d["jobs"]:
    #             jobs.extend(d["jobs"])

    for j in jobs:
        try:
            if "Engineer" in j["title"] or "Data" in j["title"] or "Support" in j["title"] or "IT" in j["title"] or "Programmer" in j["title"] or "QA" in j["title"] or "Software" in j["title"]  or "Tech " in j["title"] or "Help" in j["title"] or "Desk" in j["title"] and ("Mechnicial" not in j["title"] or "Electrical" not in j["title"]):
                # jobId = j["id"]
                # content = json.loads(requests.get(f"https://boards-api.greenhouse.io/v1/boards/{name}/jobs/{jobId}").text)["content"].replace("&lt;", "<").replace("&gt;", ">")
                # soup = BeautifulSoup(content, "lxml")
                # results = soup.find_all("ul")[1].find_all_next("li")
                # desc = [r.text.replace("&nbsp;", " ").replace("&amp;", "&").strip() for r in results] if results else None
                # desc = None

                date = datetime.strptime(j["updated_at"], "%Y-%m-%dT%H:%M:%S%z")
                position = j["title"].strip()
                company_name = company
                apply_url = j["absolute_url"].strip()
                locations_string = j["location"]["name"].strip()

                get_jobs(date, apply_url, company_name, position, locations_string, name)
        except:
            print(f"Failed on {j['title']} for {company}")

def get_url(companies: list):
    count = 1

    for name in companies:
        headers = {"User-Agent": random.choice(h.headers)}
        # try:
        url = f"https://boards-api.greenhouse.io/v1/boards/{name}/jobs"
        url2 = f"https://boards-api.greenhouse.io/v1/boards/{name}/"

        response = requests.get(url, headers=headers)
        res = requests.get(url2, headers=headers)

        if response.ok and res.ok:
            data = json.loads(response.text)
            company = json.loads(res.text)["name"]
            get_results(data, name, company)
        
            if count % 20 == 0: time.sleep(5)
            count+=1
        else:
            print(f"=> greenhouse.io: Status code {response.status_code} for {name}")

        # except:
        #     print(f"Failed to scraped: {name}")
        #     continue

def main():
    f = open(f"./data/params/greenhouse_io.txt", "r")
    companies = [company.strip() for company in f]
    f.close()

    get_url(companies)

# main()
# sys.exit(0)