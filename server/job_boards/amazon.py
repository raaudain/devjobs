import requests, json, sys, time, random
from datetime import datetime
from .modules.classes import Create_JSON, Handle_Jobs
from .modules import create_temp_json
from .modules import headers as h
# import modules.create_temp_json as create_temp_json
# import modules.headers as h


def get_jobs(date: str, url: str, company: str, position: str, location: str):
    data = create_temp_json.data
    scraped = create_temp_json.scraped

    # data = Create_Temp_JSON.data
    # scraped = Create_Temp_JSON.scraped

    post_date = datetime.timestamp(datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S"))
    
    if url not in scraped:
        data.append({
            "timestamp": post_date,
            "title": position,
            # "qualifications": qualifications,
            "company": company,
            "url": url,
            "location": location,
            "source": "Amazon",
            "source_url": "https://www.amazon.jobs",
            "category": "job"
        })
        print(f"=> amazon: Added {position} for {company}")
        scraped.add(url)
            

def get_results(item: str):
    data = item["jobs"]

    for d in data:
        if "Engineer" in d["title"] or "Data" in d["title"] or "Tech " in d["title"] or "IT" in d["title"] or "Support" in d["title"]:
            date = datetime.strptime(d["posted_date"], "%B %d, %Y")
            position = d["title"]
            # desc = d["preferred_qualifications"].replace("· ", "").replace("• ", "").split("<br/>")
            company_name = d["company_name"]
            job_path = d["job_path"].strip()
            apply_url = f"https://amazon.jobs{job_path}"
            locations_string = d["normalized_location"]

            get_jobs(date, apply_url, company_name, position, locations_string)

            # get_job = Handle_Jobs(date, apply_url, company_name, position, locations_string, "Amazon", "https://www.amazon.jobs", "amazon")
            # get_job.add_job()

def get_url():
    page = 0
    count = 0

    while count < 500:
        headers = {"User-Agent": random.choice(h.headers), "Referer":
        "https://amazon.jobs/en/search?offset=0&result_limit=100&sort=relevant&category%5B%5D=operations-it-support-engineering&category%5B%5D=software-development&distanceType=Mi&radius=24km&latitude=&longitude=&loc_group_id=&loc_query=&base_query=Operations%2C%20IT%2C%20%26%20Support%20Engineering&city=&country=&region=&county=&query_options=&"}
        url = f"https://amazon.jobs/en/search.json?category[]=operations-it-support-engineering,software-development&radius=24km&facets[]=location,business_category,category,schedule_type_id,employee_class,normalized_location,job_function_id&offset={page}0&result_limit=100&sort=relevant&latitude=&longitude=&loc_group_id=&loc_query=&base_query=Operations, IT, & Support Engineering&city=&country=&region=&county=&query_options=&="
        response = requests.get(url, headers=headers)

        if response.ok:
            data = json.loads(response.text)
            get_results(data)
            if page % 10 == 0: time.sleep(5)
            page+=1
            count+=1
        else:
            print(f"=> amazon: Failed on page {page}. Status code: {response.status_code}.")
            break


def main():
    get_url()

# main()
# sys.exit(0)