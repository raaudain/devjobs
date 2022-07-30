from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import sys, re, time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from .helpers import create_temp_json
from .helpers import driver
# import modules.create_temp_json as create_temp_json
# import modules.driver as driver

scraped = create_temp_json.scraped
data = create_temp_json.data

driver = driver.phantom

# options = webdriver.FirefoxOptions()
# browser = webdriver.Firefox(executable_path=driver, options=options)
browser = webdriver.PhantomJS(executable_path=driver)

wait = WebDriverWait(browser, 30)

isTrue = True

def getJobs(date, title, company, url, location):
    global isTrue

    date = date
    title = title
    company = company
    url = "https://stackoverflow.com"+url
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
    elif "hours" in date or "hour" in date or "h" in date:
        hours = re.sub("[^0-9]", "", date)
        time = datetime.now() - timedelta(hours=int(hours))
        date = datetime.strftime(time, "%Y-%m-%d %H:%M")
    elif "a day ago" or "yesterday" in date:
        time = datetime.now() - timedelta(days=1)
        date = datetime.strftime(time, "%Y-%m-%d %H:%M")
    elif "days" in date or "day" in date or "d" in date:
        day = re.sub("[^0-9]", "", date)
        time = datetime.now() - timedelta(days=int(day))
        date = datetime.strftime(time, "%Y-%m-%d %H:%M")

    # print(date)
    
    age = datetime.timestamp(datetime.now() - timedelta(days=14))
    post_date = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d %H:%M"))

    if age <= post_date and url not in scraped:
        data.append({
            "timestamp": post_date,
            "title": title,
            "company": company,
            "url": url,
            "location": location,
            "source": "StackOverflow",
            "source_url": "https://stackoverflow.com/",
            "category": "job"
        })
        print(f"=> stackoverflow: Added {title} for {company}")
    else:
        print(f"=> stackoverflow: Reached limit. Stopping scrape")
        isTrue = False
        
    
    scraped.add(url)

def getResults(item):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all("div", {"class": "grid--cell fl1"})

    for r in results:
        date = r.find("span", {"class": "fc-orange-400 fw-bold"}).text.strip()
        title = r.find("a", {"class": "s-link stretched-link"}, href=True).text.strip()
        company = r.find("h3", {"class": "fc-black-700 fs-body1 mb4"}).find("span").text.strip()
        url = r.find("a", {"class": "s-link stretched-link"}, href=True)["href"]
        location = r.find("span", {"class": "fc-black-500"}).text.strip()
        getJobs(date, title, company, url, location)

def getURL():    
    page = 1

    while isTrue:
        try:
            # if countdown <= 0:
            #     print("=> stackoverflow: Too many Exceptions. Stopping scrape.")
            #     break

            if page % 10 == 0:
                time.sleep(10)
                print("=> Sleeping...")

            url = f"https://stackoverflow.com/jobs?sort=p&pg={page}"

            browser.get(url)
            
            wait.until(EC.presence_of_element_located((By.XPATH, "//*[@class='s-link stretched-link']")))

            response = browser.find_element_by_xpath("//*").get_attribute("outerHTML")
            
            # print(response)
            print("stackoverflow => Page", page)

            getResults(response)
            
            # time.sleep(5)

            page+=1
       
        except:
            print(f"=> stackoverflow: Shutting down")
            # countdown-=1
            break
        
    browser.quit()

        
def main():
    getURL()
    
# main()

# sys.exit(0)