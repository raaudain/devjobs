from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests, sys, json


f = open(f"./data/craigslist/us_and_ca.txt", "r")
locations = [location.rstrip() for location in f]
f.close()

m = open(f"./data/craigslist/miami.txt", "r")
miamis = [miami.rstrip() for miami in m]
m.close()

data = []

def createJSON(item):
    with open("./data/temp/temp_data.json", "a", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def getGigs(item):
    for gig in item:
        date = gig.find("time", {"class": "result-date"})["datetime"]
        title = gig.find("a", {"class": "result-title hdrlnk"}).text
        url = gig.find("a", href=True)["href"]
        area = str(gig.find("span", {"class": "result-hood"})).replace('<span class="result-hood"> (', "").replace(")</span>", "")
        
        age = datetime.timestamp(datetime.now() - timedelta(days=7))
        postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d %H:%M"))

        if age <= postDate:
            # createJSON(postDate, title, url, area, "gig")
            data.append({
                "timestamp": postDate,
                "title": title,
                "url": url,
                "area": area,
                "category": "gig"
            })
            print(f"craigslist_gigs: Added {title}")

def getResults(item):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all("div", {"class": "result-info"})
    getGigs(results)

def getURL(items):
    for location in items:
        url = f"https://{location}.craigslist.org/d/computer-gigs/search/cpg?lang=en"
        response = requests.get(url).text
        getResults(response)

def getURLMiami(items):
    for location in items:
        url = f"{location}d/computer-gigs/search/cpg?lang=en"
        response = requests.get(url).text
        getResults(response)

def main():
    getURL(locations)
    getURLMiami(miamis)
    createJSON(data)

main()

sys.exit(0)
