from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json, requests, sys, re, time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from .modules import create_temp_json
from .modules import driver
# import modules.create_temp_json as create_temp_json
# import modules.driver as driver


data = create_temp_json.data

driver = driver.firefox

options = webdriver.FirefoxOptions()
browser = webdriver.Firefox(executable_path=driver, options=options)
# browser = webdriver.PhantomJS(executable_path=driver)

wait = WebDriverWait(browser, 30)

isTrue = True
count = 1
def getJobs(item):
    global isTrue

    for job in item:
        # print(job)
        date = job.find("div", {"class": "icon-label info-label age"}).text
        title = job.find("h2", {"class": "job-title"}).text.strip()
        company = job.find("div", {"class": "icon-label info-label company-title"}).text.strip()
        url = job.find("a", href=True)["href"]
        location = None

        if job.find("div", {"class", "icon-label info-label location"}):
            location = job.find("div", {"class", "icon-label info-label location"}).text.strip()
        if job.find("div", {"class", "icon-label info-label remote"}):
            location = job.find("div", {"class", "icon-label info-label remote"}).text.strip()

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

        if age <= postDate:
            data.append({
                "timestamp": postDate,
                "title": title,
                "company": company,
                "url": url,
                "location": location,
                "source": "BuiltIn",
                "source_url": "https://builtin.com/",
                "category": "job"
            })
            print(f"=> builtin: Added {title} for {company}")
        else:
            print(f"=> builtin: Reached limit. Stopping scrape")
            isTrue = False

def getResults(item):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all("div", {"class": "job-item"})
    filtered = []

    for result in results:
        notFeatured = result.find("div", {"class", "icon-label info-label age"})
        if notFeatured:
            filtered.append(result)

    results = filtered
    # print(results)
    getJobs(results)

def getURL():    
    page = 1
    countdown = 10

    while isTrue:
        try:
            # if countdown <= 0:
            #     print("=> builtin: Too many Exceptions. Stopping scrape.")
            #     break

            # if page % 10 == 0:
            #     time.sleep(10)
            #     print("=> Sleeping...")

            url = f"https://builtin.com/jobs/dev-engineering?page={page}"

            browser.get(url)
            
            wait.until(EC.presence_of_element_located((By.XPATH, "//*[@class='icon-label info-label age']")))

            response = browser.find_element_by_xpath("//*").get_attribute("outerHTML")
            
            # print(response)

            getResults(response)

            page+=1
            global count

            print("Page", count)
            count+=1        
        except:
            print(f"=> builtin: Countdown to shutdown: {countdown}")
            countdown-=1
            break
        
    browser.quit()

        
def main():
    getURL()
    
# main()

# sys.exit(0)