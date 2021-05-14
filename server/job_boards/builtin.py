from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json, requests, sys, re, time
from .modules import create_temp_json
from .modules import driver
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# import modules.create_temp_json as create_temp_json
# import modules.driver as driver


data = create_temp_json.data
exclude = set()
exclude.add("month")
exclude.add("months")

driver = driver.driver

options = webdriver.FirefoxOptions()
options.add_argument("--headless")
browser = webdriver.Firefox(executable_path=driver, options=options)
# browser = webdriver.PhantomJS(executable_path=driver, service_args=['--ignore-ssl-errors=true'])

wait = WebDriverWait(browser, 30)

isTrue = True
count = 1
def getJobs(item):
    global isTrue

    for job in item:
        # print(job)
        date = job.find("div", {"class", "icon-label info-label age"}).text
        title = job.find("h2", {"class": "job-title"}).text
        company = job.find("div", {"class": "icon-label info-label company-title"}).text
        url = job.find("a", href=True)["href"]
        location = None

        if job.find("div", {"class", "icon-label info-label location"}):
            location = job.find("div", {"class", "icon-label info-label location"}).text
        if job.find("div", {"class", "icon-label info-label remote"}):
            location = job.find("div", {"class", "icon-label info-label remote"}).text

        if "minutes" in date or "minute" in date:
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
            # print("day ===>",day)
            if int(day) > 7:
                isTrue = False
                browser.quit()
                print("Exit")

            time = datetime.now() - timedelta(days=int(day))
            date = datetime.strftime(time, "%Y-%m-%d %H:%M")

        
        age = datetime.timestamp(datetime.now() - timedelta(days=7))
        postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d %H:%M"))

        if age <= postDate:
            data.append({
                "timestamp": postDate,
                "title": title.strip(),
                "company": company,
                "url": url,
                "location": location.strip(),
                "source": "BuiltIn",
                "soure_url": "https://builtin.com/",
                "category": "job"
            })
            print(f"=> builtin: Added {title}")

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
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}
    

    bypassRecaptcha = "http://webcache.googleusercontent.com/search?q=cache:"
    
    page = 1

    while page <= 200:
        if page % 10 == 0:
            time.sleep(10)
            print("=> Sleeping...")

        url = f"https://builtin.com/jobs/dev-engineering?page={page}"

        browser.get(url)
        
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Featured')]")))

        response = browser.find_element_by_xpath("//*").get_attribute("outerHTML")
        
        # print(response)

        getResults(response)
        # page+=1
        # global count
        # print("Page", count)
        # count+=1

        
        # browser.quit()

def main():
    getURL()

# main()

# sys.exit(0)