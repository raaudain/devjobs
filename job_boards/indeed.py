from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json, requests


f = open(f"./data/craigslist/zip_codes.txt", "r")
codes = [code.rstrip() for code in f]
f.close()

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
        date = job.find("span", {"class": "date date-a11y"}).text.replace("\n", "")
        title = job.find("a", {"data-tn-element": "jobTitle"}).text.replace("\n", "")
        company = job.find("a", {"data-tn-element": "companyName"}).text.replace("\n", "")
        url = "https://www.indeed.com"+job.find("a", href=True)["href"]
        area = job.find("span", {"class": "location accessible-contrast-color-location"}).text
        
        # age = datetime.timestamp(datetime.now() - timedelta(days=7))
        # postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d %H:%M"))

        if date == "Just added" or date == "Today":
            date = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d %H:%M"))

        if company == False:
            company = None
        # if age <= postDate and url not in scraped:
        data.append({
            "timestamp": date,
            "title": title,
            "company": company,
            "url": url,
            "area": area,
            "category": "job"
        })
        print(f"indeed: Added {title}")
        scraped.add(url)
        # print(scraped)

def getResults(item):
    print(item)
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all("div", {"class": "jobsearch-SerpJobCard unifiedRow row result clickcard"})
    print(results)
    getJobs(results)

def getURL(items):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    ua=UserAgent()
    hdr = {'User-Agent': ua.random,
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
      'Accept-Encoding': 'none',
      'Accept-Language': 'en-US,en;q=0.8',
      'Connection': 'keep-alive'
    }

    for code in items:
        url = f"https://www.indeed.com/jobs?q=Developer&l={code}&radius=10&sort=date"
        response = requests.get(url, headers=hdr).text
        getResults(response)

def main():
    getURL(codes)
    createJSON(data)

main()

sys.exit(0)