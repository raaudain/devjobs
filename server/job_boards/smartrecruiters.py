from datetime import datetime
import requests, sys, json, time
from .modules import create_temp_json
# import modules.create_temp_json as create_temp_json


data = create_temp_json.data


f = open(f"./data/params/smartrecruiters.txt", "r")
companies = [company.strip() for company in f]
f.close()

def getJobs(date, url, company, position, location):
    date = str(date)
    title = position
    company = company
    url = url
    location = location

    postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))

    data.append({
        "timestamp": postDate,
        "title": title,
        "company": company,
        "url": url,
        "location": location,
        "source": company,
        "source_url": f"https://careers.smartrecruiters.com/{company}/",
        "category": "job"
    })
    print(f"=> smartrecruiters: Added {title} for {company}")

            


def getResults(item, name):
    data = item["content"]

    for i in data:
        if "Engineer" in i["name"] or "IT" in i["name"] or "Programmer" in i["name"] or "Data" in i["name"] or "Help" in i["name"] or "Desk" in i["name"]:
            date = datetime.strptime(i["releasedDate"], "%Y-%m-%dT%H:%M:%S.%fZ")
            jobId = i["id"]
            company_name = i["company"]["name"]
            apply_url = f"https://jobs.smartrecruiters.com/{name}/{jobId}"
            position = i["name"]
            city = f'{i["location"]["city"]}, '
            region = f'{i["location"]["region"]}, ' if "region" in i["location"] else ""
            country = i["location"]["country"].upper()
            remote = " / Remote" if i["location"]["remote"] else ""
            locations_string = f"{city}{region}{country}{remote}"
            getJobs(date, apply_url, company_name, position, locations_string)

    # for i in item:
    #     try:
    #         if "Engineer" in i["text"] or "Tech " in i["text"] or "Web" in i["text"] or "IT" in i["text"] or "Engineer" in i["categories"]["team"] or "Engineer" in i["categories"]["department"]:
    #             # use true division by 1e3 (float 1000)
    #             date = datetime.fromtimestamp(i["createdAt"] / 1e3)
    #             apply_url = i["hostedUrl"].strip()
    #             company_name = name
    #             position = i["text"].strip()
    #             locations_string = i["categories"]["location"].strip()
                
    #             getJobs(date, apply_url, company_name, position, locations_string)
    #     except:
    #         continue

def getURL():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"}

    count = 1

    for name in companies:

        url = f"https://api.smartrecruiters.com/v1/companies/{name}/postings/"

        response = requests.get(url, headers=headers)
        
        try:
            data = json.loads(response.text)

            getResults(data, name)

            if count % 5 == 0:
                time.sleep(5)


            # print(response.status_code, count)
            count += 1
        except:
            print(f"Failed to scraped: {name}")
        
    
    # url = f"https://api.smartrecruiters.com/v1/companies/Zscaler/postings/"

    # response = requests.get(url, headers=headers).text

    # data = json.loads(response)

    # getResults(data)
    
    # print(data)


def main():
    getURL()

# main()
# sys.exit(0)