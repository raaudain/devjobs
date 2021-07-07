from datetime import datetime
import requests, sys, json, time
from .modules import create_temp_json
# import modules.create_temp_json as create_temp_json


data = create_temp_json.data
scraped = create_temp_json.scraped

f = open(f"./data/params/lever_co.txt", "r")
companies = [company.strip() for company in f]
f.close()

def getJobs(date, url, company, position, location):
    date = str(date)
    title = position
    company = company
    url = url
    location = location

    postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f"))

    if url not in scraped:
        data.append({
            "timestamp": postDate,
            "title": title,
            "company": company.replace("get", "").replace("join", "").capitalize(),
            "url": url,
            "location": location,
            "source": company.replace("get", "").replace("join", "").capitalize(),
            "source_url": f"https://jobs.lever.co/{company}",
            "category": "job"
        })
        scraped.add(url)
        print(f"=> lever.co: Added {title} for {company}")
    else:
        print(f"=> lever.co: Already scraped {title} for {company}")
            


def getResults(item, name):
    for i in item:
        try:
            if "Engineer" in i["text"] or "Tech " in i["text"] or "Web" in i["text"] or "IT" in i["text"] or "Engineer" in i["categories"]["team"] or "Engineer" in i["categories"]["department"]:
                # use true division by 1e3 (float 1000)
                date = datetime.fromtimestamp(i["createdAt"] / 1e3)
                apply_url = i["hostedUrl"].strip()
                company_name = name
                position = i["text"].strip()
                locations_string = i["categories"]["location"].strip()
                
                getJobs(date, apply_url, company_name, position, locations_string)
        except:
            continue

def getURL():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"}

    count = 1

    for name in companies:

        url = f"https://api.lever.co/v0/postings/{name}/"

        response = requests.get(url, headers=headers)

        if response.ok:

            data = json.loads(response.text)

            getResults(data, name)

            if count % 5 == 0:
                time.sleep(5)


            # print(response.status_code, count)
            count += 1
        else:
            print(f"Failed to scraped: {name}")
            
    
    # url = f"https://api.lever.co/v0/postings/preset"

    # response = requests.get(url, headers=headers).text

    # data = json.loads(response)

    # getResults(data, "preset")
    
    # print(data)


def main():
    getURL()

# main()
# sys.exit(0)