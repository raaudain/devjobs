from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# from .modules import create_temp_json
# from .modules import driver
import modules.create_temp_json as create_temp_json
import modules.driver as driver
import sys, time


driver = driver.firefox

data = create_temp_json.data

options = webdriver.FirefoxOptions()
# options.add_argument("--headless")
browser = webdriver.Firefox(executable_path=driver, options=options)

wait = WebDriverWait(browser, 30)

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
    results = soup.find_all("li", {"data-job-id":True})

    print(results)

    for i in results:
        date = datetime.strftime(datetime.now(), "%Y-%m-%d")
        apply_url = "https://jobs.target.com"+i["href"]
        company_name = "Target"
        position = i.find("h2").text.strip()
        locations_string = i.find("span", class_="job-location").text.strip()
        
        print(date, apply_url, company_name, position, locations_string)

def getURL():
    # while True:
        # if EC.presence_of_element_located((By.XPATH, "//a[@class='next disabled']")):
        #     break

        
    url = f"https://jobs.target.com/search-jobs?ac=67611"

    browser.get(url)

    wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='job-location']")))

    time.sleep(15)

    response = browser.find_element_by_xpath("//*").get_attribute("outerHTML")

    getResults(response)
        

        # browser.find_element_by_id("pagination-current-bottom").send_keys(2)
        
        # browser.find_element_by_xpath("*//[@class='pagination-page-jump']").click()
        # wait.until(EC.invisibility_of_element_located((By.XPATH, "//*[@id='ccpa-button']"))).

        # wait.until(EC.presence_of_element_located((By.XPATH, "//*[@class='next']"))).click()

    browser.quit()
    
    # print(response)

def main():
    getURL()

main()
sys.exit(0)