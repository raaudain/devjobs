import requests, json, sys
from datetime import datetime
from bs4 import BeautifulSoup
from .modules import create_temp_json
# import modules.create_temp_json as create_temp_json



def get_jobs(date: str, url: str, company: str, position: str, location: str):
    data = create_temp_json.data
    post_date = datetime.timestamp(datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S"))
    
    data.append({
        "timestamp": post_date,
        "title": position,
        # "qualifications": qualifications,
        "company": company,
        "url": url,
        "location": location,
        "source": company,
        "source_url": "https://careers.nintendo.com",
        "category": "job"
    })
    print(f"=> nintendo: Added {position} for {company}")


def get_results(item: str):
    for data in item:
        if "Software" in data["JobDescription"] or "IT " in data["JobTitle"] or "Support" in data["JobTitle"]:
            date = datetime.strptime(data["JobCreationDate"], "%B %d, %Y")
            job_id = data["JobId"]
            apply_url = f"https://careers.nintendo.com/job-openings/listing/{job_id}.html"
            company_name = "Nintendo of America"
            position = data["JobTitle"].strip()
            # results = BeautifulSoup(data["ExternalQualificationHTML"], "lxml").find_all("li")
            # desc = [i.text.replace("\n\xa0\nNOA-RG", "").strip() for i in results if "Such as" not in i.text]
            # desc = None
            locations_string = f"{data['JobPrimaryLocationCode']}, {data['JobLocationStateAbbrev']}".strip()

            get_jobs(date, apply_url, company_name, position, locations_string)
        

def get_url():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36", "Origin": "https://careers.nintendo.com"}
    url = f"https://2oc84v7py6.execute-api.us-west-2.amazonaws.com/prod/api/jobs/"
    response = requests.get(url, headers=headers)

    if response.ok:
        data = json.loads(response.text)
        get_results(data)
    else:
        print("=> nintendo: Error - Response status", response.status_code)


def main():
    get_url()


# main()
# sys.exit(0)