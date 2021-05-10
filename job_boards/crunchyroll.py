from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests
import modules.create_temp_json as create_temp_json


data = create_temp_json.data

def getJobs(item):
    for job in item:
        date = datetime.strftime(datetime.now(), "%Y-%m-%d")
        title = job.find("p", {"class": "open-position--job-title"}).text
        company = job.find("a")["data-company"]
        url = job.find("a", href=True)["href"]
        region = job.find("div", {"class": "open-position--job-information"}).find_all("p")[0].text

        postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d"))

        if title not in exclude:
            data.append({
                "timestamp": postDate,
                "title": title,
                "company": company,
                "url": url,
                "region": region,
                "category": "job"
            })
            print(f"=> key_values: Added {title}")

def getResults(item):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find("ul", {"class": "job-list"}).find_all("li")
    print(results)
    # getJobs(results)

def getURL():
    referer = "https://www.google.com/"
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36", "referer": referer}

    bypassRecaptcha = "http://webcache.googleusercontent.com/search?q=cache:"
    url = f"{bypassRecaptcha}https://www.crunchyroll.com/about/jobs/index.html"
    response = requests.get(url=url, headers=headers).text

    # print(response)
    getResults(response)

def main():
    getURL()

main()