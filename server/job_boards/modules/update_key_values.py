from bs4 import BeautifulSoup
import requests
from os.path import isfile


def main():
    if isfile("./data/params/key_values.txt"):
        print("=> key_values: Deleting old parameters")
        t = open(f"./data/temp/temp_data.json", "r+")
        t.truncate(0)
        t.close()

    url = "https://www.keyvalues.com/"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "lxml")

    company = open("./data/params/key_values.txt", "w")

    links = soup.find_all("a", {"class": "thumbnail-link"}, href=True)

    for link in links:
        company.write(link["href"]+"\n")
    print("=> key_values: Updated parameters")
    company.close()

