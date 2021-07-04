from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json, requests, sys, re, time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# from .modules import create_temp_json
# from .modules import driver
import modules.create_temp_json as create_temp_json
import modules.driver as driver


data = create_temp_json.data
scraped = create_temp_json.scraped

driver = driver.firefox

options = webdriver.FirefoxOptions()
# webdriver.DesiredCapabilities.FIREFOX["phantomjs.page.customHeaders.User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0"
browser = webdriver.Firefox(executable_path=driver, options=options)
# browser = webdriver.PhantomJS(executable_path=driver)

wait = WebDriverWait(browser, 30)

isTrue = True
count = 1
def getJobs(date, title, company, url, location):
    global isTrue


    date = date
    title = title
    company = company
    url = "https://www.indeed.com"+url
    location = location

    print(date, title)

    if "a second ago" in date or "just" in date.toLowerCase():
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
    elif "today" in date.toLowerCase():
        time = datetime.now()
        date = datetime.strftime(time, "%Y-%m-%d %H:%M")
    elif "a day ago" in date or "yesterday" in date.toLowerCase():
        time = datetime.now() - timedelta(days=1)
        date = datetime.strftime(time, "%Y-%m-%d %H:%M")
    elif "days" in date or "day" in date:
        day = re.sub("[^0-9]", "", date)
        time = datetime.now() - timedelta(days=int(day))
        date = datetime.strftime(time, "%Y-%m-%d %H:%M")

    print(date, title, company, location, url)
    
    age = datetime.timestamp(datetime.now() - timedelta(days=7))
    postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d %H:%M"))

    # if {"date": date, "title": title, "company": company} not in scraped:
    if age <= postDate:
        data.append({
            "timestamp": postDate,
            "title": title,
            "company": company,
            "url": url,
            "location": location,
            "source": "Indeed",
            "source_url": "https://www.indeed.com/",
            "category": "job"
        })
        print(f"=> indeed: Added {title} for {company}")
            # scraped.add({"date": date, "title": title, "company": company})
    else:
        print(f"=> indeed: Reached limit. Stopping scrape")
        isTrue = False


def getResults(item):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all("a", {"data-hide-spinner": "true"})

    for result in results:
        url = result["href"]
        title = result.find("span", title=True).text.strip()
        company = result.find("span", {"class": "companyName"}).text.strip()
        location = result.find("div", {"class": "companyLocation"}).text.strip()
        date = result.find("span", {"class": "date"}).text.strip()

        # if "pagead" not in result.find("div", {"class": "companyLocation"}).text:
        #     location = result.find("div", {"class": "companyLocation"}).text
        # else:
        #     location = None

        print(date, title, company, url, location)
        # print(date)

    # results = filtered
    # print(results)
    # getJobs(results)

def getURL():    
    page = 0

    while isTrue:
        try:
            # if countdown <= 0:
            #     print("=> builtin: Too many Exceptions. Stopping scrape.")
            #     break

            # if page % 10 == 0:
            #     time.sleep(10)
            #     print("=> Sleeping...")

            url = f"https://www.indeed.com/jobs?q=developer&sort=date&start={page}0"

            browser.get(url)
            
            # wait.until(EC.presence_of_element_located((By.XPATH, "//*[@class='companyName']")))
            time.sleep(10)
            response = browser.find_element_by_xpath("//*").get_attribute("outerHTML")
            
            # print(response)

            getResults(response)
            # break
            page+=1
            global count

            print("Page", count)
            count+=1        
        except:
            break
        
    browser.quit()

        
def main():
    getURL()
    
main()

sys.exit(0)