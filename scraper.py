from bs4 import BeautifulSoup
import requests

urls = []
results = []
gigs = []

f = open(f"./locations.txt", "r")
locations = [location.rstrip() for location in f]
f.close()

for location in locations:
    url = f"https://{location}.craigslist.org/d/computer-gigs/search/cpg?lang=en"
    urls.append(requests.get(url).text)

for url in urls:
    # print(url)
    soup = BeautifulSoup(url, "lxml")
    results.append(soup.find_all("div", {"class" : "result-info"}))
    # print(results)

for result in results:
    for x in result:
        # print(j)
        date = x.find("time", {"class" : "result-date"})["datetime"]
        title = x.find("a", {"class" : "result-title hdrlnk"}).text
        url = x.find("a", href=True)["href"]
        area = str(x.find("span", {"class" : "result-hood"})).replace('<span class="result-hood"> (', "").replace(")</span>", "")
            
        gigs.append({"date": date, "title": title, "url": url, "area": area})
