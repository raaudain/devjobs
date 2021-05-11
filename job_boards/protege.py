from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json, requests, sys
import modules.create_temp_json as create_temp_json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import modules.driver as driver


driver = driver.driver

options = webdriver.FirefoxOptions()
options.add_argument("--headless")
browser = webdriver.Firefox(executable_path=driver, options=options)

wait = WebDriverWait(browser, 10)

data = create_temp_json.data

def getJobs(item):
    for job in item:
        date = datetime.strftime(datetime.now(), "%Y-%m-%d")
        title = job.find("h2").text
        company = job.find("p").text
        url = "https://protege.dev"+job["href"]
        region = "Remote"

        postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d"))

        print(date, title, company, url, region)


        data.append({
            "timestamp": postDate,
            "title": title,
            "company": company,
            "url": url,
            "region": region,
            "category": "job"
        })
        print(f"=> protege: Added {title}")

def getResults(item):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find("div", {"data-cy": "job-board-list"}).find_all("a", href=True)
    
    # print(results)
    getJobs(results)

def getURL():
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}

    url = f"https://protege.dev/job-board"
    response = requests.get(url, headers=headers).text
    browser.get(url)
    
    wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Front-End')]")))

    response = browser.find_element_by_xpath("//*").get_attribute("outerHTML")

    # print(response)
    getResults(response)
    browser.quit()

def main():
    getURL()

main()
sys.exit(0)