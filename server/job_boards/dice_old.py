from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from selenium import webdriver
import sys, time, re
from .modules import create_temp_json
from .modules import driver
# import modules.driver as driver
# import modules.create_temp_json as create_temp_json


driver = driver.firefox

data = create_temp_json.data
scraped = create_temp_json.scraped


browser = webdriver.Firefox(executable_path=driver)

jobs = ["developer", "software engineer", "devops engineer", "support engineer", "frontend engineer", "backend", "fullstack", "it engineer"]

def getJobs(date, title, company, url, location):
    date = date
    title = title
    company = company
    url = url
    location = location

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
    post_date = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d %H:%M"))

    if title and company and location not in scraped:
        if age <= post_date:
            data.append({
                "timestamp": post_date,
                "title": title,
                "company": company,
                "url": url,
                "location": location,
                "source": "Dice",
                "source_url": "https://www.dice.com",
                "category": "job"
            })
            print(f"=> dice: Added {title} for {company}")
        scraped.add(title)
        scraped.add(company)
        scraped.add(location)

def getResults(item):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all("div", {"class": "card search-card"})

    for result in results:
        date = result.find("span", class_="posted-date").text.strip()
        title = result.find("a", class_="card-title-link bold", href=True).text.strip()
        company = result.find("a", class_="ng-star-inserted", href=True).text.strip()
        url = result.find("a", class_="card-title-link bold", href=True)["href"]
        location = result.find("span", id="searchResultLocation").text.strip()

        getJobs(date, title, company, url, location)
    

def getURL():
    # url = f"https://www.dice.com/jobs?q=developer&countryCode=US&radius=30&radiusUnit=mi&page=1&pageSize=1000&filters.postedDate=SEVEN&language=en"

    # browser.get(url)

    # time.sleep(15)

    # response = browser.find_element_by_xpath("//*").get_attribute("outerHTML")
        
    # getResults(response)


    for job in jobs:
        url = f"https://www.dice.com/jobs?q={job}&countryCode=US&radius=30&radiusUnit=mi&page=1&pageSize=1000&filters.postedDate=SEVEN&filters.employerType=Direct Hire&language=en"

        browser.get(url)

        time.sleep(15)

        response = browser.find_element_by_xpath("//*").get_attribute("outerHTML")
        
        getResults(response)
        # print(response)

    browser.quit()

        


def main():
    getURL()
    

# main()
# sys.exit(0)