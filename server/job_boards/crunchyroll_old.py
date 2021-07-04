from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# import modules.create_temp_json as create_temp_json
# import modules.driver as driver
from .modules import create_temp_json
from .modules import driver
import sys


driver = driver.firefox

data = create_temp_json.data

# webdriver.DesiredCapabilities.FIREFOX["phantomjs.page.customHeaders.User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0"
# webdriver.DesiredCapabilities.PHANTOMJS["phantomjs.page.customHeaders.Referrer"] = "https://www.google.com"
# browser = webdriver.PhantomJS(executable_path=driver, )
options = webdriver.FirefoxOptions()
# options.add_argument("--headless")
browser = webdriver.Firefox(executable_path=driver, options=options)

wait = WebDriverWait(browser, 30)

def getJobs(item):
    for job in item:
        date = datetime.strftime(datetime.now(), "%Y-%m-%d")
        title = job.find("a", href=True).text.strip()
        company = "Crunchyroll"
        url = job.find("a", href=True)["href"]
        location = job.find("span", {"class": "location"}).text.strip()

        postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d"))

        data.append({
            "timestamp": postDate,
            "title": title,
            "company": company,
            "url": url,
            "location": location,
            "source": "Crunchyroll",
            "source_url": "https://www.crunchyroll.com/about/jobs/index.html",
            "category": "job"
        })
        print(f"=> crunchyroll: Added {title}")

def getResults(item):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all("li", {"class": "job-list-item"})

    for result in results:
        if result.find("h4").text.strip() == "Engineering":
            results = result.find("ul")

    getJobs(results)

def getURL():
    


    bypassRecaptcha = "http://webcache.googleusercontent.com/search?q=cache:"
    url = f"https://www.crunchyroll.com/about/jobs/index.html"

    browser.get(url)
    
    wait.until(EC.presence_of_element_located((By.XPATH, "//li[@class='positions-list-item']")))

    response = browser.find_element_by_xpath("//html").get_attribute("outerHTML")
    
    browser.quit()
    getResults(response)
    # print(response)


def main():
    getURL()
            

# main()
# sys.exit(0)