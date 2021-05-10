import modules.create_temp_json as create_temp_json
from parsel import Selector
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


data = create_temp_json.data

driver = "./bin/geckodriver-mac"

fireFoxOptions = webdriver.FirefoxOptions()
fireFoxOptions.set_headless()
browser = webdriver.Firefox(executable_path=driver, firefox_options=fireFoxOptions)

wait = WebDriverWait(browser, 10)

def getJobs(item):
    for job in item:
        date = datetime.strftime(datetime.now(), "%Y-%m-%d")
        title = job.find("a", href=True).text.strip()
        company = "Crunchyroll"
        url = job.find("a", href=True)["href"]
        region = job.find("span", {"class": "location"}).text.strip()

        postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d"))

        data.append({
            "timestamp": postDate,
            "title": title,
            "company": company,
            "url": url,
            "region": region,
            "category": "job"
        })
        print(f"=> key_values: Added {title}")

def getResults(item):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all("li", {"class": "job-list-item"})

    for result in results:
        if result.find("h4").text.strip() == "Engineering":
            results = result.find("ul")

    getJobs(results)

def getURL():
    bypassRecaptcha = "http://webcache.googleusercontent.com/search?q=cache:"
    url = f"{bypassRecaptcha}https://www.crunchyroll.com/about/jobs/index.html"

    browser.get(url)
    
    wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Engineering')]")))

    response = browser.find_element_by_xpath("//*").get_attribute("outerHTML")
    
    getResults(response)
    browser.quit()

def main():
    getURL()
