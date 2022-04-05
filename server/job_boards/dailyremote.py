from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests, sys, re, time
# from .modules import create_temp_json
import modules.create_temp_json as create_temp_json


data = create_temp_json.data
isTrue = True

def getJobs(item):
    global isTrue

    for job in item:
        date = job.find_all("span", {"class": "company-name display-flex"})
        title = job.find("h2", {"class": "job-position"}).text.strip()
        company = job.find("span", {"class": "company-name display-flex"})
        link = job.find("a", {"class": "primary-btn apply-link"}, href=True)["href"].strip()
        url = None
        logo = "https://dailyremote.com"+job.find(class_="pic")["src"] if job.find(class_="pic") else None
        location = job.find_all("span", {"class": "meta-holder"})[0].text.strip()

        print(date, title, company, link, location, logo)

        if "apply" in link:
            url = "https://dailyremote.com"+link
        else:
            url = link

        if "a second ago" in date:
            time = datetime.now() - timedelta(seconds=1)
            date = datetime.strftime(time, "%Y-%m-%d %H:%M")
        elif "seconds" in date or "second" in date:
            seconds = re.sub("[^0-9]", "", date)
            time = datetime.now() - timedelta(seconds=int(seconds))
            date = datetime.strftime(time, "%Y-%m-%d %H:%M")
        elif "a minute ago" in date:
            time = datetime.now() - timedelta(minutes=1)
            date = datetime.strftime(time, "%Y-%m-%d %H:%M")
        elif "minutes" in date or "minute" in date:
            minutes = re.sub("[^0-9]", "", date)
            time = datetime.now() - timedelta(minutes=int(minutes))
            date = datetime.strftime(time, "%Y-%m-%d %H:%M")
        elif "an hour ago" in date:
            time = datetime.now() - timedelta(hours=1)
            date = datetime.strftime(time, "%Y-%m-%d %H:%M")
        elif "hours" in date or "hour" in date:
            hours = re.sub("[^0-9]", "", date)
            time = datetime.now() - timedelta(hours=int(hours))
            date = datetime.strftime(time, "%Y-%m-%d %H:%M")
        elif "a day ago" in date:
            time = datetime.now() - timedelta(days=1)
            date = datetime.strftime(time, "%Y-%m-%d %H:%M")
        elif "days" in date or "day" in date:
            day = re.sub("[^0-9]", "", date)
            time = datetime.now() - timedelta(days=int(day))
            date = datetime.strftime(time, "%Y-%m-%d %H:%M")
        
        age = datetime.timestamp(datetime.now() - timedelta(days=7))
        postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d %H:%M"))
        
        print(date, title, company, url, location)




        if age <= postDate:
            data.append({
                "timestamp": postDate,
                "title": title,
                "company": company,
                "url": url,
                "location": location,
                "source": "Daily Remote",
                "source_url": f"https://dailyremote.com",
                "category": "job"
            })
            print(f"=> dailyremote: Added {title} for {company}")
        else:
            print(f"=> dailyremote: Reached limit. Stopping scrape")
            isTrue = False

def getResults(item):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all("article")

    print(results)
    getJobs(results)

def getURL():
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0"}

    # url = f"https://dailyremote.com/remote-software-development-jobs?search=&page=224&sort_by=time#main"
    # response = requests.get(url, headers=headers).text
    # getResults(response)

    page = 1

    while isTrue:
        if isTrue == False:
            break

        # if page % 5 == 0:
        #     time.sleep(2)
        print(f"=> dailyremote: Scraping page {page}")

        # try:
        url = f"https://dailyremote.com/remote-software-development-jobs?search=&page={page}&sort_by=time#main"
        response = requests.get(url, headers=headers).text
        getResults(response)
        
        time.sleep(5)
        page += 1
        print(response)
        # except:
        #     print(f"=> dailyremote: Continue to page {page}")
        #     continue


def main():
    getURL()

main()
sys.exit(0)