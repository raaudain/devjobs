from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sys, time
# from .modules import create_temp_json
# from .modules import driver
import modules.driver as driver
import modules.create_temp_json as create_temp_json


driver = driver.driver

data = create_temp_json.data

# options = webdriver.FirefoxOptions()
# options.add_argument("--headless")
# browser = webdriver.Firefox(executable_path=driver, options=options)
browser = webdriver.PhantomJS(executable_path=driver)

wait = WebDriverWait(browser, 10)

def getJobs(item):



    for job in item:
        print(job)
        date = datetime.strftime(datetime.now(), "%Y-%m-%d")
        title = job.find("a", href=True).text.strip()
        company = "Crunchyroll"
        url = job.find("a", href=True)["href"]
        location = job.find("span", {"class": "location"}).text.strip()

        age = datetime.timestamp(datetime.now() - timedelta(days=7))
        postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d"))

        data.append({
            "timestamp": postDate,
            "title": title,
            "company": company,
            "url": url,
            "location": location,
            "source": "Dice",
            "source_url": "https://www.crunchyroll.com/about/jobs/index.html",
            "category": "job"
        })
        print(f"=> crunchyroll: Added {title}")

def getResults(item):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all("div", {"class": "card search-card"})

    # for result in results:
    #     if result.find("h4").text.strip() == "Engineering":
    #         results = result.find("ul")
    
    getJobs(results)

def getURL():
    referer = "https://www.google.com"
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36", "referer": referer}


    bypassRecaptcha = "http://webcache.googleusercontent.com/search?q=cache:"
    url = f"https://www.dice.com/jobs?q=developer&countryCode=US&radius=30&radiusUnit=mi&page=1&pageSize=1000&filters.postedDate=SEVEN&language=en"

    browser.get(url)
    
    wait.until(EC.presence_of_element_located((By.XPATH, "//*[@class='card search-card')]")))

    response = browser.find_element_by_xpath("//*").get_attribute("outerHTML")
    
    # getResults(response)
    print(url)
    # browser.quit()


def main():
    getURL()

# main()
# sys.exit(0)