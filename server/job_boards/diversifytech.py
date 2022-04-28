import requests, json, sys, random
from datetime import datetime
from .modules import create_temp_json
from .modules import headers as h
# import modules.create_temp_json as create_temp_json
# import modules.headers as h


def get_jobs(date: str, url: str, company: str, position: str, location: str, logo: str):
    data = create_temp_json.data
    scraped = create_temp_json.scraped

    post_date = datetime.timestamp(datetime.strptime(str(date), "%Y-%m-%dT%H:%M:%S.%fZ"))
    
    data.append({
        "timestamp": post_date,
        "title": position,
        "company": company,
        "company_logo": logo,
        "url": url,
        "location": location,
        "source": "Diversify Tech",
        "source_url": "https://www.diversifytech.co/",
        "category": "job"
    })
    scraped.add(company)
    print(f"=> diversifytech: Added {position}")


def get_results(item: str):
    for i in item:
        job = i["node"]["data"]
        date = job["Created_Date"]
        position = job["Role"].strip()
        company_name = job["Company"][0]["data"]["Name"].strip()
        logo = job["Company"][0]["data"]["Logo"][0]["thumbnails"]["large"]["url"]
        apply_url = "https://www.diversifytech.co/job-board/"+job["Job_ID"]
        locations_string = job["Location"].strip()

        get_jobs(date, apply_url, company_name, position, locations_string, logo)


def get_url():
        try:
            headers = {"User-Agent": random.choice(h.headers)}
            url = f"https://www.diversifytech.co/page-data/job-board/page-data.json"
            response = requests.get(url, headers=headers)
            data = json.loads(response.text)["result"]["data"]["allAirtable"]["edges"]

            if len(data) > 0:               
                get_results(data)         
        except:
            print(f"=> diversifytech: Status code: {response.status_code}.")



def main():
    get_url()


# main()
# sys.exit(0)