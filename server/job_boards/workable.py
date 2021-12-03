from datetime import datetime
import requests, json, sys, time, random, asyncio
from .modules.classes import Page_Not_Found
from .modules.headers import headers as h
from .modules import create_temp_json
# import modules.create_temp_json as create_temp_json
# import modules.headers as headers


data = create_temp_json.data
scraped = create_temp_json.scraped
# header = headers.headers

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
    scraped.add(company)
    print(f"=> workable: Added {title} for {company}")


def getResults(item, param, company):
    jobs = item["results"]

    for data in jobs:
        if "Software " in data["title"] or "Support " in data["title"] or "Front" in data["title"] or "Data " in data["title"] or "Back" in data["title"] or "Full" in data["title"] or "QA" in data["title"] or "IT " in data["title"] or "ML" in data["title"]or "Tech " in data["title"] or "devops" in data["title"].lower():
            date = datetime.strptime(data["published"], "%Y-%m-%dT%H:%M:%S.%fZ")
            apply_url = f"https://apply.workable.com/{param}/j/{data['shortcode']}/"
            company_name = company.strip()
            position = data["title"].strip()
            state = f"{data['location']['city']}, {data['location']['region']}, "
            locations_string = f"{state if data['location']['city'] else ''}{data['location']['country']}"
            
            getJobs(date, apply_url, company_name, position, locations_string, param)
        

async def getURL():

    count = 1

    for company in companies:
        token = "0"

        try:
            while token:
                headers = {"User-Agent": random.choice(h)}
                url = f"https://apply.workable.com/api/v3/accounts/{company}/jobs"
                url2 = f"https://apply.workable.com/api/v1/accounts/{company}"
                payload = {
                    "query":"engineer, developer",
                    "location":[],
                    "department":[],
                    "worktype":[],
                    "remote":[],
                    "token":token
                }

                response = requests.post(url, json=payload, headers=headers)
                # if response.ok:
                if response.status_code == 404:
                    not_found = Page_Not_Found("./data/params/workable.txt", company)
                    not_found.remove_unwanted()

                data = json.loads(response.text)
                name = json.loads(requests.get(url2, headers=headers).text)["name"]

                getResults(data, company, name)

                if "nextPage" in data: token = data["nextPage"]
                else: token = ""
                
                if count % 5 == 0: await asyncio.sleep(10)
                
                count+=1

                

        except:
            print(f"=> workable: Failed for {company}. Status code: {response.status_code}.")
            pass
        


def main():
    getURL()

# main()
# sys.exit(0)