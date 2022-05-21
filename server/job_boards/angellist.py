from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dateutil import relativedelta
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# import modules.create_temp_json as create_temp_json
from .modules import create_temp_json
import sys, re, time





wait = WebDriverWait(browser, 15)

data = create_temp_json.data

f = open(f"./data/params/angellist.txt", "r")
companies = [company.strip() for company in f]
f.close()

def getJobs(item, company):
    for job in item:
        date = job.find("h6", {"class": "styles_component__1kg4S styles_flair__pwHYF __halo_textContrast_dark_A __halo_fontSizeMap_size--xs __halo_fontWeight_medium styles_uppercase__382zl"}).text.strip()
        title = job.find("h4", {"class": "styles_component__1kg4S styles_flow__3_K06 styles_jobTitle__2ELW6 __halo_fontSizeMap_size--lg __halo_fontWeight_medium"}).text.strip()
        company = company
        url = "https://angel.co"+job.find("a", href=True)["href"]
        location = job.find("div", {"class": "styles_component__26gqE styles_truncate__dUufp styles_location__ACesY"}).text.strip()

        if "a second ago" in date:
            time = datetime.now() - timedelta(seconds=1)
            date = datetime.strftime(time, "%Y-%m-%d")
        elif "seconds" in date or "second" in date:
            seconds = re.sub("[^0-9]", "", date)
            time = datetime.now() - timedelta(seconds=int(seconds))
            date = datetime.strftime(time, "%Y-%m-%d")
        elif "a minute ago" in date:
            time = datetime.now() - timedelta(minutes=1)
            date = datetime.strftime(time, "%Y-%m-%d")
        elif "minutes" in date or "minute" in date:
            minutes = re.sub("[^0-9]", "", date)
            time = datetime.now() - timedelta(minutes=int(minutes))
            date = datetime.strftime(time, "%Y-%m-%d")
        elif "an hour ago" in date:
            time = datetime.now() - timedelta(hours=1)
            date = datetime.strftime(time, "%Y-%m-%d")
        elif "hours" in date or "hour" in date:
            hours = re.sub("[^0-9]", "", date)
            time = datetime.now() - timedelta(hours=int(hours))
            date = datetime.strftime(time, "%Y-%m-%d")
        elif "today" in date:
            time = datetime.now()
            date = datetime.strftime(time, "%Y-%m-%d")
        elif "a day ago" in date or "yesterday" in date:
            time = datetime.now() - timedelta(days=1)
            date = datetime.strftime(time, "%Y-%m-%d")
        elif "days" in date or "day" in date:
            day = re.sub("[^0-9]", "", date)
            time = datetime.now() - timedelta(days=int(day))
            date = datetime.strftime(time, "%Y-%m-%d")
        elif "weeks" in date or "week" in date:
            week = re.sub("[^0-9]", "", date)
            time = datetime.now() - timedelta(weeks=int(week))
            date = datetime.strftime(time, "%Y-%m-%d")
        elif "month" in date or "months" in date:
            month = re.sub("[^0-9]", "", date)
            time = datetime.now() - relativedelta.relativedelta(months=int(month))
            date = datetime.strftime(time, "%Y-%m-%d")
        

        # print(date, title, company, url, location)
        post_date = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d"))

        data.append({
            "timestamp": post_date,
            "title": title,
            "company": company,
            "url": url,
            "location": location,
            "source": "AngelList",
            "source_url": "https://angel.co",
            "category": "job"
        })
        print(f"=> angellist: Added {title} for {company}")

def getResults(item):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all("div", {"class": "styles_component__1_YxE styles_expanded__31zII"})
    company = soup.find("a", {"class": "styles_component__1c6JC styles_defaultLink__1mFc1 styles_anchor__2aXMZ"}).text
    jobs = []

    for result in results:
        if result.find("h6").text.strip() == "Engineering":
            jobs.append(result)

    results = jobs

    getJobs(results, company)
    # print(results, company)

def getURL():
    # index = 0

    # for company in companies:
    #     try:
    #         captcha = wait.until(EC.presence_of_element_located((By.XPATH, "//iframe")))

    #         if captcha:
    #             break

    #         url = f"https://angel.co/company/{company}/jobs"

    #         browser.get(url)
    
    #         wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='styles_component__1_YxE styles_expanded__31zII']")))

    #         response = browser.find_element_by_xpath("//html").get_attribute("outerHTML")
    
        
    #         getResults(response)

    #         index += 1
    #     except:
    #         print(f"=> angellist: No dev jobs for {company}. Continue to {companies[index]}")
    #         continue

    # browser.quit()

    url = f"https://angel.co/company/lucid-motors-2/jobs"

    browser.get(url)
    
    wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='styles_component__1_YxE styles_expanded__31zII']")))

    response = browser.find_element_by_xpath("//html").get_attribute("outerHTML")
    
    browser.quit()
    getResults(response)
    # print(response)


def main():
    getURL()


main()
sys.exit(0)