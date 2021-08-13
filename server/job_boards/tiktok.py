from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from .modules import create_temp_json
from .modules import driver
# import modules.create_temp_json as create_temp_json
# import modules.driver as driver
import sys


driver = driver.firefox

data = create_temp_json.data
scraped = create_temp_json.scraped

options = webdriver.FirefoxOptions()
options.add_argument("--headless")
browser = webdriver.Firefox(executable_path=driver, options=options)

wait = WebDriverWait(browser, 30)

def getJobs(date, apply_url, company_name, position, locations_string):
    date = str(date)
    title = position
    company = company_name
    url = apply_url
    location = locations_string

    postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d"))

    if url not in scraped:
        data.append({
            "timestamp": postDate,
            "title": title,
            "company": company,
            "url": url,
            "location": location,
            "source": company,
            "source_url": "https://careers.tiktok.com/",
            "category": "job"
        })
        scraped.add(url)
        print(f"=> tiktok: Added {title}")

def getResults(item):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all("a", {"data-id":True})

    for i in results:
        date = datetime.strftime(datetime.now(), "%Y-%m-%d")
        apply_url = "https://careers.tiktok.com"+i["href"]
        company_name = "TikTok"
        position = i.find("span", class_="positionItem-title-text").text.strip()
        locations_string = i.find("div", class_="subTitle__3sRa3 positionItem-subTitle").contents[0]
        
        getJobs(date, apply_url, company_name, position, locations_string)

def getURL():
    keywords = ["engineer", "data ", "developer"] 

    for keyword in keywords:
        try:
            url = f"https://careers.tiktok.com/position?keywords={keyword}&category=&location=&project=&type=&job_hot_flag=&current=1&limit=1000"

            browser.get(url)
            

            wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='positionItem__1giWi positionItem']")))

            response = browser.find_element_by_xpath("//html").get_attribute("outerHTML")

            getResults(response)
        except:
            print(f"=> Failed to scrape TikTok for {keyword}")

    browser.quit()
    
    # print(response)

def main():
    getURL()

# main()
# sys.exit(0)