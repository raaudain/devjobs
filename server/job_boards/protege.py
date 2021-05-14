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
        date = datetime.strptime(job.find("p", {"class": "text-lg font-bold text-teal-700"}).text+" "+str(datetime.today().year), "%b %d %Y")
        title = job.find("h2").text
        company = job.find("p").text
        url = "https://protege.dev"+job["href"]
        location = "Remote"

        # print(date, title, company, url, location)

        age = datetime.timestamp(datetime.now() - timedelta(days=7))
        postDate = datetime.timestamp(datetime.strptime(str(date)[:-9], "%Y-%m-%d"))

        if age <= postDate:
            data.append({
                "timestamp": postDate,
                "title": title,
                "company": company,
                "url": url,
                "location": location,
                "source": "Protege",
                "source_url": "https://protege.dev",
                "category": "job"
            })
            print(f"=> protege: Added {title}")

def getResults(item):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find("div", {"data-cy": "job-card-container"}).find_all("a", href=True)
    
    # print(results)
    getJobs(results)

def getURL():
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}

    url = f"https://protege.dev"
    response = requests.get(url, headers=headers).text
    browser.get(url)
    
    wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Latest Opportunities')]")))

    response = browser.find_element_by_xpath("//*").get_attribute("outerHTML")

    # print(response)
    getResults(response)
    browser.quit()

def main():
    getURL()

# main()
# sys.exit(0)