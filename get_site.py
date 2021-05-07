from bs4 import BeautifulSoup
import requests


url = "https://www.keyvalues.com/"
html = requests.get(url).text
soup = BeautifulSoup(html, "lxml")

company = open("./data/craigslist/key_values.txt", "w")

links = soup.find_all("a", {"class": "thumbnail-link"}, href=True)

for link in links:
    company.write(link["href"]+"\n")

company.close()