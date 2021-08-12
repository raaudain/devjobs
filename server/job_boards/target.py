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

options = webdriver.FirefoxOptions()
options.add_argument("--headless")
browser = webdriver.Firefox(executable_path=driver, options=options)

wait = WebDriverWait(browser, 10)

isTrue = True

def getJobs(date, apply_url, company_name, position, locations_string):
    date = str(date)
    title = position
    company = company_name
    url = apply_url
    location = locations_string

    postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d"))

    data.append({
        "timestamp": postDate,
        "title": title,
        "company": company,
        "url": url,
        "location": location,
        "source": company,
        "source_url": "https://corporate.target.com/careers/corporate",
        "category": "job"
    })
    print(f"=> target: Added {title}")

def getResults(item):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find("section", {"id":"search-results-list"}).find_all("li")

    for i in results:
        if i.find("h2"):
            date = datetime.strftime(datetime.now(), "%Y-%m-%d")
            apply_url = "https://jobs.target.com"+i.find("a", href=True)["href"]
            company_name = "Target"
            position = str(i.find("h2")).replace("<h2>", "").replace("</h2>", "").replace("&amp;", "&").strip()
            locations_string = str(i.find("span", class_="job-location")).replace('<span class="job-location">', "").replace("</span>", "").strip()
            
            getJobs(date, apply_url, company_name, position, locations_string)

def getURL():
    page = 1

    while isTrue:
        try:
            url = f"https://jobs.target.com/search-jobs?ac=67611&p={page}"

            browser.get(url)
            print("target cookies =>", browser.get_cookies())
            wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='job-location']")))

            response = browser.find_element_by_xpath("//*").get_attribute("outerHTML")

            getResults(response)
            
            page+=1
        except:
            break
        
    browser.quit()


    
    # print(response)

def main():
    getURL()

# main()
# sys.exit(0)