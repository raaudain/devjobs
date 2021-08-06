from datetime import datetime
import requests, json, sys, time
from .modules import create_temp_json
# import modules.create_temp_json as create_temp_json


data = create_temp_json.data

f = open(f"./data/params/workable.txt", "r")
companies = [company.strip() for company in f]
f.close()

def getJobs(date, url, company, position, location, param):
    date = str(date)
    title = position
    company = company
    url = url
    location = location

    # print(date, title, company, url, location)

    postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))
    
    data.append({
        "timestamp": postDate,
        "title": title,
        "company": company,
        "url": url,
        "location": location,
        "source": company,
        "source_url": f"https://apply.workable.com/{param}/",
        "category": "job"
    })
    print(f"=> workable: Added {title} for {company}")


def getResults(item, param, company):
    jobs = item["results"]

    # print(jobs)

    for data in jobs:
        if "Software " in data["title"] or "Support " in data["title"] or "Front" in data["title"] or "Data " in data["title"] or "Back" in data["title"] or "Full" in data["title"] or "QA" in data["title"] or "IT " in data["title"] or "ML" in data["title"]or "Tech " in data["title"] or "devops" in data["title"].lower():
            date = datetime.strptime(data["published"], "%Y-%m-%dT%H:%M:%S.%fZ")
            apply_url = f"https://apply.workable.com/{param}/j/{data['shortcode']}/"
            company_name = company.strip()
            position = data["title"].strip()
            state = f"{data['location']['city']}, {data['location']['region']}, "
            locations_string = f"{state if data['location']['city'] else ''}{data['location']['country']}"
            
            getJobs(date, apply_url, company_name, position, locations_string, param)
        

def getURL():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"}

    count = 1

    for company in companies:
        try:
            token = "0"

            while token:
                url = f"https://apply.workable.com/api/v3/accounts/{company}/jobs"
                url2 = f"https://apply.workable.com/api/v1/accounts/{company}"
                payload = {
                    "query":"engineer",
                    "location":[],
                    "department":[],
                    "worktype":[],
                    "remote":[],
                    "token":token
                }

                response = requests.post(url, json=payload, headers=headers).text

                data = json.loads(response)
                name = json.loads(requests.get(url2, headers=headers).text)["name"]

                getResults(data, company, name)

                if "nextPage" in data:
                    token = data["nextPage"]
                else:
                    token = ""
                
                if count % 5 == 0:
                    time.sleep(5)
                
                count+=1

        except:
            print(f"=> workable: Failed for {company}")
            continue
        


def main():
    getURL()

# main()
# sys.exit(0)