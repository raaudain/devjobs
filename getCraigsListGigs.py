from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests
import sys


f = open(f"./locations.txt", "r")
locations = [location.rstrip() for location in f]
f.close()

m = open(f"./miami.txt", "r")
miamis = [miami.rstrip() for miami in m]
m.close()

gigs = []

def getGigs(item):
    for gig in item:
        date = gig.find("time", {"class": "result-date"})["datetime"]
        title = gig.find("a", {"class": "result-title hdrlnk"}).text
        url = gig.find("a", href=True)["href"]
        area = str(gig.find("span", {"class": "result-hood"})).replace('<span class="result-hood"> (', "").replace(")</span>", "")
        
        age = datetime.timestamp(datetime.now() - timedelta(days=7))
        postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d %H:%M"))
        
        if age <= postDate:
            g = {"date": date, "title": title, "url": url, "area": area}
            f = open(f"./data/data.txt", "a")
            f.write(f"{g}\n")
            f.close()

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

main()

sys.exit(0)
# print(gigs)

