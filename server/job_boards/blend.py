from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json, requests, sys
from .modules import create_temp_json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from .modules import driver


driver = driver.driver

options = webdriver.FirefoxOptions()
options.add_argument("--headless")
browser = webdriver.Firefox(executable_path=driver, options=options)
# browser = webdriver.PhantomJS(executable_path=driver)


wait = WebDriverWait(browser, 10)

data = create_temp_json.data

def getJobs(item):
    for job in item:
        date = datetime.strftime(datetime.now(), "%Y-%m-%d")
        title = job.find("a", href=True).text.strip()
        company = "Blend"
        url = job.find("a", href=True)["href"]
        region = None

        postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d"))

        data.append({
            "timestamp": postDate,
            "title": title,
            "company": company,
            "url": url,
            "region": region,
            "category": "job"
        })
        print(f"=> blend: Added {title}")

def getResults(item):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find("ol", {"class": "blend-lever-jobs"}).find_all("li")

    for result in results:
        if result.find("h4"):
            if result.find("h4").text.strip() == "Engineering":
                results = result.find_all("li", {"class": "job-title"})
    
    getJobs(results)

def getURL():
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}

    url = f"https://blend.com/company/careers/#current-openings"
    response = requests.get(url, headers=headers).text
    browser.get(url)
    
    wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Engineering')]")))

    response = browser.find_element_by_xpath("//*").get_attribute("outerHTML")

    getResults(response)
    browser.quit()

def main():
    getURL()

# main()
# sys.exit(0)