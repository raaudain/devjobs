from datetime import datetime
from bs4 import BeautifulSoup
import requests, sys, json, time, random
from .modules.headers import headers as h
from .modules import create_temp_json
from .modules.classes import List_Of_Companies, Page_Not_Found
# import modules.create_temp_json as create_temp_json
# import modules.headers as headers


FILE_PATH = "./data/params/smartrecruiters.txt"

def get_jobs(date: str, url: str, company: str, position: str, location: str, logo: str, name: str):
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
        "source_url": f"https://careers.smartrecruiters.com/{name}/",
        "category": "job"
    })
    scraped.add(company)
    print(f"=> smartrecruiters: Added {position} for {company}")


def get_results(item: str, name: str):
    data = item["content"]
    images = {}

    if data:
        for i in data:
            if "Engineer" in i["name"] or "IT " in i["name"] or "Programmer" in i["name"] or "Data" in i["name"] or "Help" in i["name"] or "Desk" in i["name"] or "Developer" in i["name"] and ("Elect" not in i["name"] and "Mechanical" not in i["name"] and "Front Desk Associates" not in i["name"]):
                date = datetime.strptime(i["releasedDate"], "%Y-%m-%dT%H:%M:%S.%fZ")
                jobId = i["id"]
                company_name = i["company"]["name"]
                apply_url = f"https://jobs.smartrecruiters.com/{name}/{jobId}"
                logo = None
                
                if name in images:
                    logo = images[name]
                else:
                    try:
                        r = requests.get(apply_url)
                        if r.ok:
                            soup = BeautifulSoup(r.text, "lxml")
                            if soup.find(class_="header-logo logo").find("img", src=True):
                                logo = soup.find(class_="header-logo logo").find("img")["src"]
                                images[name] = logo
                            else:
                                logo = None
                    except:
                        print(f"Unable to get logo for {name}")

                position = i["name"]
                city = f'{i["location"]["city"]}, '
                region = f'{i["location"]["region"]}, ' if "region" in i["location"] else ""
                country = i["location"]["country"].upper()
                remote = " | Remote" if i["location"]["remote"] else ""
                locations_string = f"{city}{region}{country}{remote}"

                get_jobs(date, apply_url, company_name, position, locations_string, logo, name)
    else:
        print(f"=> smartrecruiters: No jobs for {name}.")


def get_url(companies: list):
    count = 1

    for name in companies:
        headers = {"User-Agent": random.choice(h)}
        url = f"https://api.smartrecruiters.com/v1/companies/{name}/postings/"
        # url = f"https://api.smartrecruiters.com/v1/companies/Zscaler/postings/"
        response = requests.get(url, headers=headers)
        
        if response.ok:
            data = json.loads(response.text)
            get_results(data, name)
            if count % 10 == 0: time.sleep(5)
            count += 1
        elif response.status_code == 404:
            not_found = Page_Not_Found(FILE_PATH, name)
            not_found.remove_not_found()
        else:
            print(f"=> smartrecruiters: Failed to scraped {name}. Status code: {response.status_code}.")


def main():
    companies = List_Of_Companies(FILE_PATH).read_file()
    get_url(companies)


# main()
# sys.exit(0)