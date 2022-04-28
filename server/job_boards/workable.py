from datetime import datetime
import requests, json, sys, time, random
from .modules.classes import List_Of_Companies, Page_Not_Found
from .modules.headers import headers as h
from .modules import create_temp_json
# import modules.create_temp_json as create_temp_json
# import modules.headers as h
# import modules.classes as c


FILE_PATH = "./data/params/workable.txt"

def get_jobs(date: str, url: str, company: str, position: str, location: str, logo: str, param: str):
    data = create_temp_json.data
    scraped = create_temp_json.scraped

    postDate = datetime.timestamp(datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S"))
    
    data.append({
        "timestamp": postDate,
        "title": position,
        "company": company,
        "company_logo": logo,
        "url": url,
        "location": location,
        "source": company,
        "source_url": f"https://apply.workable.com/{param}/",
        "category": "job"
    })
    scraped.add(company)
    print(f"=> workable: Added {position} for {company}")


def get_results(item: str, param: str, company: str, logo: str):
    jobs = item["results"]

    for data in jobs:
        if "Software " in data["title"] or "Support " in data["title"] or "Front" in data["title"] or "Data " in data["title"] or "Back" in data["title"] or "Full" in data["title"] or "QA" in data["title"] or "IT " in data["title"] or "ML" in data["title"]or "Tech " in data["title"] or "devops" in data["title"].lower():
            date = datetime.strptime(data["published"], "%Y-%m-%dT%H:%M:%S.%fZ")
            apply_url = f"https://apply.workable.com/{param}/j/{data['shortcode']}/"
            company_name = company.strip()
            position = data["title"].strip()
            state = f"{data['location']['city']}, {data['location']['region']}, "
            locations_string = f"{state if data['location']['city'] else ''}{data['location']['country']}"
            
            get_jobs(date, apply_url, company_name, position, locations_string, logo, param)
        

def get_url(companies: list):
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
                    not_found = Page_Not_Found(FILE_PATH, company)
                    not_found.remove_unwanted()
                
                info = requests.get(url2, headers=headers).text

                data = json.loads(response.text)
                name = json.loads(info)["name"].strip()
                logo = json.loads(info)["logo"] if "logo" in json.loads(info) else None

                get_results(data, company, name, logo)

                if "nextPage" in data: token = data["nextPage"]
                else: token = ""
                
                if count % 1 == 0: time.sleep(5)
                
                count+=1    
        except:
            print(f"=> workable: Failed for {company}. Status code: {response.status_code}.")


def main():
    companies = List_Of_Companies(FILE_PATH).open_file()
    get_url(companies)


# main()
# sys.exit(0)
