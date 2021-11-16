import requests, json, sys, time, random
from datetime import datetime, timedelta
from .modules import create_temp_json
from .modules import headers as h
# import modules.create_temp_json as create_temp_json
# import modules.headers as h


IS_TRUE = True

def get_jobs(date: str, url: str, company: str, position: str, location: str):
    global IS_TRUE

    data = create_temp_json.data
    scraped = create_temp_json.scraped
    
    age = datetime.timestamp(datetime.now() - timedelta(days=30))
    post_date = datetime.timestamp(datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S"))
    
    if url not in scraped:
        if age <= post_date:
            data.append({
                "timestamp": post_date,
                "title": position,
                "company": company,
                "url": url,
                "location": location,
                "source": "Builtin",
                "source_url": "https://builtin.com/",
                "category": "job"
            })
            scraped.add(url)
            print(f"=> builtin: Added {position} for {company}")
        else:
            print(f"=> builtin: Reached limit. Stopping scrape")
            IS_TRUE = False


def get_results(item: str):
    jobs = item["jobs"]
    companies = item["companies"]

    # Remove unwanted data
    for i in range(len(companies)):
        # if "company_perks" in companies[i]: del companies[i]["company_perks"]
        # if "elite" in companies[i]: del companies[i]["elite"]
        # if "high_volume_poster" in companies[i]: del companies[i]["high_volume_poster"]
        # if "company_perks" in companies[i]: del companies[i]["job_slots"]
        # if "company_perks" in companies[i]: del companies[i]["limited_listing"]
        # if "company_perks" in companies[i]: del companies[i]["logo"]
        # if "company_perks" in companies[i]: del companies[i]["premium"]
        # if "company_perks" in companies[i]: del companies[i]["region_id"]
        companies[i]["company"] = companies[i]["title"]

    for i in range(len(jobs)):
        # del jobs[i]["category_id"]
        # del jobs[i]["body"]
        # del jobs[i]["experience_level"]
        # del jobs[i]["hot_jobs_score"]
        # del jobs[i]["is_national"]
        # del jobs[i]["meta_tags"]
        # del jobs[i]["remote"]
        # del jobs[i]["remote_status"]
        # del jobs[i]["body_summary"]
        # del jobs[i]["industry_id"]
        # del jobs[i]["sub_category_id"]
        # del jobs[i]["id"]
        jobs[i]["id"] = jobs[i]["company_id"]
        
    # Merge dictionaries by id
    data = {d["id"]: d for d in companies}
    for j in jobs: data[j["id"]].update(j)

    scraped = create_temp_json.scraped

    for d in list(data.values()):
        if d["company"] not in scraped:
            date = datetime.strptime(d["sort_job"], "%a, %d %b %Y %H:%M:%S GMT")
            position = d["title"]
            base_url = None

            if d["region_id"] == 1: base_url = "https://www.builtinchicago.org"
            elif d["region_id"] == 2: base_url = "https://www.builtincolorado.com"
            elif d["region_id"] == 3: base_url = "https://www.builtinla.com"
            elif d["region_id"] == 4: base_url = "https://www.builtinaustin.com"
            elif d["region_id"] == 5: base_url = "https://www.builtinnyc.com"
            elif d["region_id"] == 6: base_url = "https://www.builtinboston.com"
            elif d["region_id"] == 7: base_url = "https://www.builtinseattle.com"
            else: base_url = "https://www.builtinsf.com"
            
            apply_url = f"{base_url}{d['alias']}"
            company_name = d["company"]
            locations_string = d["location"]

            get_jobs(date, apply_url, company_name, position, locations_string)


def get_url():
    page = 1

    while IS_TRUE:
        if IS_TRUE == False: break

        headers = {"User-Agent":random.choice(h.headers), "Origin":"https://builtin.com","Referer":"https://builtin.com/"}
        url = f"https://api.builtin.com/services/job-retrieval/legacy-jobs/?categories=149&subcategories=&experiences=&industry=&regions=&locations=&remote=2&per_page=1000&page={page}&search=&sortStrategy=recency&jobs_board=true&national=false"
        response = requests.get(url, headers=headers)

        if response.ok:
            data = json.loads(response.text)
            get_results(data)
            # if page % 1 == 0: time.sleep(5)
            page+=1
        else:
            print(f"=> builtin: Failed on page {page}. Status code: {response.status_code}.")
            break


def main():
    get_url()

# main()
# sys.exit(0)