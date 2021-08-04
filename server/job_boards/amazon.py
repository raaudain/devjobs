from datetime import datetime, timedelta
import requests, json, sys, time
from .modules import create_temp_json
# import modules.create_temp_json as create_temp_json


data = create_temp_json.data
scraped = create_temp_json.scraped

def getJobs(date, url, company, position, location, qualifications):
    date = str(date)
    title = position
    qualifications = qualifications
    company = company
    url = url
    location = location

    # age = datetime.timestamp(datetime.now() - timedelta(days=7))
    postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))
    
    if url not in scraped:
        data.append({
            "timestamp": postDate,
            "title": title,
            "qualifications": qualifications,
            "company": company,
            "url": url,
            "location": location,
            "source": "Amazon",
            "source_url": "https://www.amazon.jobs",
            "category": "job"
        })
        print(f"=> amazon: Added {title} for {company}")
        scraped.add(url)
            

def getResults(item):
    data = item["jobs"]

    for d in data:
        if "Engineer" in d["title"] or "Data" in d["title"] or "Tech " in d["title"] or "IT" in d["title"] or "Support" in d["title"]:
            date = datetime.strptime(d["posted_date"], "%B %d, %Y")
            position = d["title"]
            desc = d["preferred_qualifications"].replace("· ", "").replace("• ", "").split("<br/>")
            company_name = d["company_name"]
            jobPath = d["job_path"].strip()
            apply_url = f"https://amazon.jobs{jobPath}"
            locations_string = d["normalized_location"]

            getJobs(date, apply_url, company_name, position, locations_string, desc)


def getURL():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36", "Referer":
	"https://amazon.jobs/en/search?offset=0&result_limit=100&sort=relevant&category%5B%5D=operations-it-support-engineering&category%5B%5D=software-development&distanceType=Mi&radius=24km&latitude=&longitude=&loc_group_id=&loc_query=&base_query=Operations%2C%20IT%2C%20%26%20Support%20Engineering&city=&country=&region=&county=&query_options=&"}

    page = 0
    count = 0

    while count < 500:
        try:
            url = f"https://amazon.jobs/en/search.json?category[]=operations-it-support-engineering,software-development&radius=24km&facets[]=location,business_category,category,schedule_type_id,employee_class,normalized_location,job_function_id&offset={page}0&result_limit=100&sort=relevant&latitude=&longitude=&loc_group_id=&loc_query=&base_query=Operations, IT, & Support Engineering&city=&country=&region=&county=&query_options=&="

            response = requests.get(url, headers=headers).text
            data = json.loads(response)

            getResults(data)
            # print(data)
            if page % 10 == 0:
                time.sleep(5)
                    
            page+=1
            count+=1

        except:
            print(f"Failed on page {page}")
            break

def main():
    getURL()

# main()
# sys.exit(0)