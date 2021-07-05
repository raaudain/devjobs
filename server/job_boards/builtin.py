from datetime import datetime, timedelta
import requests, json, sys, time
from .modules import create_temp_json
# import modules.create_temp_json as create_temp_json


data = create_temp_json.data
scraped = create_temp_json.scraped

isTrue = True

def getJobs(date, url, company, position, location):
    global isTrue

    date = str(date)
    title = position
    company = company
    url = url
    location = location

    
    age = datetime.timestamp(datetime.now() - timedelta(days=7))
    postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))
    
    if url not in scraped:
        if age <= postDate:
            data.append({
                "timestamp": postDate,
                "title": title,
                "company": company,
                "url": url,
                "location": location,
                "source": "Builtin",
                "source_url": "https://builtin.com/",
                "category": "job"
            })
            print(f"=> builtin: Added {title} for {company}")
            scraped.add(url)
        else:
            print(f"=> builtin: Reached limit. Stopping scrape")
            isTrue = False


def getResults(item):
    jobs = item["jobs"]
    companies = item["companies"]

    # Remove unwanted data
    for i in range(len(companies)):
        del companies[i]["company_perks"]
        del companies[i]["elite"]
        del companies[i]["high_volume_poster"]
        del companies[i]["job_slots"]
        del companies[i]["limited_listing"]
        del companies[i]["logo"]
        del companies[i]["premium"]
        del companies[i]["region_id"]
        companies[i]["company"] = companies[i]["title"]

    for i in range(len(jobs)):
        del jobs[i]["category_id"]
        del jobs[i]["body"]
        del jobs[i]["experience_level"]
        del jobs[i]["hot_jobs_score"]
        del jobs[i]["is_national"]
        del jobs[i]["meta_tags"]
        del jobs[i]["remote"]
        del jobs[i]["remote_status"]
        del jobs[i]["body_summary"]
        del jobs[i]["industry_id"]
        del jobs[i]["sub_category_id"]
        del jobs[i]["id"]
        jobs[i]["id"] = jobs[i]["company_id"]
        
    # Merge dictionaries by id
    data = {d["id"]: d for d in companies}

    for j in jobs:
        data[j["id"]].update(j)

    # Loop through data
    for d in list(data.values()):
        date = datetime.strptime(d["sort_job"], "%a, %d %b %Y %H:%M:%S GMT")
        position = d["title"]
        base_url = None

        if d["region_id"] == 1:
            base_url = "https://www.builtinchicago.org"
        elif d["region_id"] == 2:
            base_url = "https://www.builtincolorado.com"
        elif d["region_id"] == 3:
            base_url = "https://www.builtinla.com"
        elif d["region_id"] == 4:
            base_url = "https://www.builtinaustin.com"
        elif d["region_id"] == 5:
            base_url = "https://www.builtinnyc.com"
        elif d["region_id"] == 6:
            base_url = "https://www.builtinboston.com"
        elif d["region_id"] == 7:
            base_url = "https://www.builtinseattle.com"
        else:
            base_url = "https://www.builtinsf.com"
        
        apply_url = f"{base_url}{d['alias']}"
        company_name = d["company"]
        locations_string = d["location"]

        getJobs(date, apply_url, company_name, position, locations_string)
        time.sleep(5)


def getURL():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"}

    page = 1

    while isTrue:
        try:
            url = f"https://api.builtin.com/services/job-retrieval/legacy-jobs/?categories=149&subcategories=&experiences=&industry=&regions=&locations=&remote=2&per_page=1000&page={page}&search=&sortStrategy=recency&jobs_board=true&national=false"

            response = requests.get(url, headers=headers).text

            data = json.loads(response)

            getResults(data)
            page+=1
        except:
            print(f"=> builtin: Break")
            break
    
    # print(data)
     


def main():
    getURL()

# main()
# sys.exit(0)