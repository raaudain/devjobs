from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests, sys, time
# from .modules import create_temp_json
import modules.create_temp_json as create_temp_json


data = create_temp_json.data

f = open(f"./data/params/jobvite.txt", "r")
companies = [company.strip() for company in f]
f.close()

def getJobs(date, apply_url, company_name, position, locations_string, name):
    date = str(date)
    title = position
    company = company_name
    url = apply_url
    location = locations_string

    # print(date, title, company, url, location, source_url)
    postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d"))

    data.append({
        "timestamp": postDate,
        "title": title,
        "company": company,
        "url": url,
        "location": location,
        "source": company,
        "source_url": f"https://jobs.jobvite.com/careers/{name}",
        "category": "job"
    })
    print(f"=> jobvite: Added {title} for {company}")

        

def getResults(item, name):
    soup = BeautifulSoup(item, "lxml")
    results = [*soup.find_all(class_="jv-job-list")]
    company = name.capitalize()
    titles = soup.find_all(class_="jv-job-list-name")
    locations = soup.find_all(class_="jv-job-list-location")

    res = []

    for t in titles:
        for l in locations:
            if titles.index(t) == locations.index(l):
                # print(t, l)
                title = t.find("a").text.strip()

                print(title, name, l)

                # if "Engineer" in title or "Tech" in title or "Web" in title or "Data " in title or "QA" in title or "Cloud" in title or "IT " in title or "Software" in "title" or "Front" in title or "Back" in title:
                #     date = datetime.strftime(datetime.now(), "%Y-%m-%d")
                #     apply_url = "https://jobs.jobvite.com"+t.find("a")["href"].strip()
                #     company_name = company
                #     position = title
                #     locations_string = l.find(class_="jv-job-list-location").text.strip()
                    
                #     print(date, apply_url, company_name, position, locations_string, name)

    # for i in [*results]:
    #     res.append(i)
    
    # for r in results:
    #     # print(r)
    #     title = r.find(class_="jv-job-list-name").text.strip()
    #     print(title, name)

    #     if "Engineer" in title or "Tech" in title or "Web" in title or "Data " in title or "QA" in title or "Cloud" in title or "IT " in title or "Software" in "title" or "Front" in title or "Back" in title:
    #         date = datetime.strftime(datetime.now(), "%Y-%m-%d")
    #         apply_url = "https://jobs.jobvite.com"+r.find("a")["href"].strip()
    #         company_name = company
    #         position = title
    #         locations_string = r.find("td", class_="jv-job-list-location").text.strip()
            
    #         getJobs(date, apply_url, company_name, position, locations_string, name)


def getURL():
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0"}

    # url = f"https://jobs.lever.co/clubhouse"
    # response = requests.get(url, headers=headers).text
    # getResults(response)
    count = 1

    for name in companies:
        # try:
        url = f"https://jobs.jobvite.com/careers/{name}"
        response = requests.get(url, headers=headers).text
        getResults(response, name)
        
        if count % 10 == 0:
            time.sleep(5)
            
        count+=1
            # print(response)
        # except:
        #     print(f"=> jobvite: Scrape failed for {name}. Going to next.")
        #     continue


def main():
    getURL()

main()
sys.exit(0)