from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests
import sys
# from .modules import create_temp_json
import modules.create_temp_json as create_temp_json


data = create_temp_json.data
scraped = create_temp_json.scraped


def getJobs(date, title, company, url):
    date = date
    title = title
    company = company
    url = "https://justremote.co"+url
    location = "Remote"
    age = datetime.timestamp(datetime.now() - timedelta(days=14))
    post_date = datetime.timestamp(datetime.strptime(date, "%Y %d %b"))
    if url not in scraped:
        if age <= post_date:
            data.append({
                "timestamp": post_date,
                "title": title,
                "company": company,
                "url": url,
                "location": location,
                "source": "JustRemote",
                "source_url": "https://justremote.co",
                "category": "job"
            })
            scraped.add(url)
            print(f"=> justremote: Added {title} for {company}")
    else:
        print(f"=> justremote: Already scraped {title} for {company}")


def getResults(item):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all(
        "div", {"class": "new-job-item__JobInnerWrapper-sc-1qa4r36-12 doExVb"})
    r = soup.find_all(
        "div", class_="new-job-item__JobInnerWrapper-sc-1qa4r36-12 doExVb")
    # results = soup.find_all("h2", {"class": "job-listings__Title-sc-8ldju0-8 bHpcli"})[1]

    print(r)
    # for result in results:
    #     date = f'{datetime.strftime(datetime.now(), "%Y")} {result.find("div", {"class": "new-job-item__JobItemDate-sc-1qa4r36-5 dmIPAp"}).text.strip()}'
    #     title = result.find("h3", {"class": "new-job-item__JobTitle-sc-1qa4r36-8 iNuReR"}).text.strip()
    #     company = result.find("div", {"class": "new-job-item__JobItemCompany-sc-1qa4r36-4 jNtqCf"}).text.strip()
    #     url = result.find("a", {"class": "new-job-item__JobMeta-sc-1qa4r36-7 eFiLvL"}, href=True)["href"]

    # getJobs(date, title, company, url)


def getURL():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0"}

    url = "https://justremote.co/remote-developer-jobs"
    response = requests.get(url, headers=headers).text

    getResults(response)
    # print(response)


def main():
    getURL()


main()
sys.exit(0)
