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

    dontAdd = ("/wealthfront", "/github", "/instacart", "/readme", "/seesaw", "/nova-credit", "/academia", "/angellist", "/honor", "/render", "/automatticcareers", "doppler", "/sparrow", "/cointracker", "/circleci", "/curai", "/qualia", "/betterup", "/modeanalytics", "/grouparoo", "/humanfirst", "/goodnotes", "/hatch", "/point", "/hipcamp", "/seesaw", "/airtable", "/covariant", "/universe", "/alto", "/jane", "/lightstep", "/digit", "/readme", "/cameo", "/gusto", "/enigma", "/handshake", "/aptible", "/newfront", "/angaza", "/launchdarkly", "/lever", "/stitchfix", "/checkr", "/stitch-fix", "/flexport", "/nexhealth", "/connected", "/flickr", "/mode", "/brex", "/culture-biosciences", "/iora-health", "/routific", "/picnichealth", "/nerdwallet", "/vanta", "/treasury-prime", "/smugmug-flickr")

    for link in links:
        if link["href"] not in dontAdd:
            company.write(link["href"]+"\n")
    print("=> key_values: Updated parameters")
    company.close()

# main()