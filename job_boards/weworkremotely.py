from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from lxml import etree
import json, requests


scraped = set()
data = []

t = open(f"./data/temp/temp_data.json", "r+")
t.truncate(0)
t.close()

def createJSON(item):
    with open("./data/temp/temp_data.json", "a", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def getJobs(item):
    for job in item:
        # date = job.find("span", {"class": "date"}).text
        # date = job.select("datetime")[0]
        date = etree.HTML(str(job))
        title = job.find("span", {"class": "title"}).text
        company = job.find("span", {"class": "company"}).text
        url = "https://www.weworkremotely.com"+job.find("a", href=True)["href"]
        region = job.find("span", {"class": "region company"}).contents[0]
        
        print(region)
        print(type(date), date.xpath("/html/body/div[3]/div/section[1]/article/ul/li[169]/a/span[3]/time")[0])
        if date == True:
            print(date)
        else:
            date = None

        print(date)
        # age = datetime.timestamp(datetime.now() - timedelta(days=7))
        # postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d %H:%M"))
        
        # if age <= postDate and url not in scraped:
        #     data.append({
        #         "timestamp": postDate,
        #         "title": title,
        #         "company": company,
        #         "url": url,
        #         "region": region,
        #         "category": "job"
        #     })
        print(f"weworkremotely: Added {title}")
        scraped.add(url)
        # print(scraped)

def getResults(item):
    soup = BeautifulSoup(item, "html.parser")
    results = soup.find("div", {"class": "content"}).find_all("li", {"class": ["feature", ""]})
    # print(results)
    getJobs(results)

def getURL():
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    # ua=UserAgent()
    # hdr = {'User-Agent': ua.random,
    #   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    #   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    #   'Accept-Encoding': 'none',
    #   'Accept-Language': 'en-US,en;q=0.8',
    #   'Connection': 'keep-alive'
    # }

    
    url = f"https://weworkremotely.com/remote-jobs/search?term=&button=&categories%5B%5D=2&categories%5B%5D=17&categories%5B%5D=18&categories%5B%5D=6"
    response = requests.get(url, headers=headers).text
    getResults(response)

def main():
    getURL()
    createJSON(data)

main()

sys.exit(0)