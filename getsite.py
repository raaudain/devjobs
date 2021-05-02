from bs4 import BeautifulSoup
import requests


url = "https://www.craigslist.org/about/sites"
html = requests.get(url).text
soup = BeautifulSoup(html, "lxml")

locations = open("locations.txt", "w")
miami = open("miami.txt", "w")

links = soup.find_all("a", href=True)

for link in links:
    if ".org" in link["href"] and "miami" not in link["href"] and "www" not in link["href"] and "forums" not in link["href"]:
        locations.write(link["href"].replace("https://", "").replace(".craigslist.org/", "")+"\n")
        
locations.close()
for link in links:
    if ".org" in link["href"] and "miami" in link["href"]:
        miami.write(link["href"]+"\n")


miami.close()

