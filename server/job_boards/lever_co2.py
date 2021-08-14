from datetime import datetime
from bs4 import BeautifulSoup
import requests, sys, json, time, random
# from .modules import create_temp_json
# from .modules import headers as h
import modules.create_temp_json as create_temp_json
import modules.headers as h

data = create_temp_json.data
scraped = create_temp_json.scraped

f = open(f"./data/params/lever_co.txt", "r")
companies = [company.strip() for company in f]
f.close()

def getJobs(date, url, company, position, location, param):
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
            "company": company,
            "url": url,
            "location": location,
            "source": company,
            "source_url": f"https://jobs.lever.co/{param}",
            "category": "job"
        })
        scraped.add(url)
        print(f"=> lever.co: Added {title} for {company}")
    else:
        print(f"=> lever.co: Already scraped {title} for {company}")
            


def getResults(item, param, company):
    for i in item:
        try:
            if "Engineer" in i["text"] or "Tech " in i["text"] or "Web" in i["text"] or "IT " in i["text"] or "Engineer" in i["categories"]["team"] or "Engineer" in i["categories"]["department"] or "Technology" in i["categories"]["department"] or "Data" in i["text"] or "Information Technology" in i["text"]:
                # use true division by 1e3 (float 1000)
                date = datetime.fromtimestamp(i["createdAt"] / 1e3)
                apply_url = i["hostedUrl"].strip()
                company_name = company
                position = i["text"].strip()
                locations_string = i["categories"]["location"].strip()
                
                getJobs(date, apply_url, company_name, position, locations_string, param)
        except:
            pass

def getURL():
    # headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"}

    count = 1

    for name in companies:
        headers = {"User-Agent": random.choice(h.headers)}
        print(headers)
        url = f"https://api.lever.co/v0/postings/{name}/"
        url2 = f"https://jobs.lever.co/{name}"

        response = requests.get(url, headers=headers)
        
        res = requests.get(url2, headers=headers)

        company = None

        if res.ok:
            company = BeautifulSoup(res.text, "lxml").title.text
        else:
            company = name.capitalize()

        if response.ok:

            data = json.loads(response.text)

            getResults(data, name, company)

            if count % 1 == 0:
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

main()
sys.exit(0)