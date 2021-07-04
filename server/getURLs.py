import requests, sys, re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import job_boards.modules.driver as driver

driver = driver.firefox

options = webdriver.FirefoxOptions()
browser = webdriver.Firefox(executable_path=driver, options=options)

wait = WebDriverWait(browser, 30)

w = open("./data/params/workable.txt", "r")
workable = [company.strip() for company in w]
w.close()

def getResults(item):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all("a", class_="title may-blank outbound", href=True)
    # print(links)
    # results = re.findall(r"https://apply.workable.com/(.*?)/", links)

    added = set()

    for r in results:
        c = re.search(r"https://apply.workable.com/(.*?)/", r["href"]).group(1)
        print(c)

        if c not in workable:
            if c not in added:
                a = open("./data/params/workable.txt", "a")
                a.write(f"{c}\n")
                a.close()
                added.add(c)


def getURL():
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}

    count = 0

    while count < 1000:

        url = f"https://www.reddit.com/domain/apply.workable.com/"
        # response = requests.get(url, headers=headers)


        browser.get(url)
    
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[@class='title may-blank outbound']")))

        response = browser.find_element_by_xpath("//html").get_attribute("outerHTML")
    
        getResults(response)

        
        # getResults(response.text)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@class='next-button']"))).click()
        # print(response.status_code)
        count+=25

    browser.quit()


def main():
    getURL()

main()
sys.exit(0)