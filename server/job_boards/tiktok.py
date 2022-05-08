import sys
import time
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from .modules import create_temp_json
from .modules import driver
from .modules.classes import Filter_Jobs
# import modules.create_temp_json as create_temp_json
# import modules.driver as driver


# options = webdriver.FirefoxOptions()
# options.add_argument("--headless")
# browser = webdriver.Firefox(executable_path=driver, options=options)

driver = driver.chrome
options = webdriver.ChromeOptions()
options.add_argument("--headless")
browser = webdriver.Chrome(executable_path=driver, options=options)
wait = WebDriverWait(browser, 30)


def get_results(item):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all("a", {"data-id": True})
    for r in results:
        date = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
        post_date = datetime.timestamp(
            datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S"))
        apply_url = "https://careers.tiktok.com"+r["href"]
        company_name = "TikTok"
        position = r.find(
            "span", class_="positionItem-title-text").text.strip()
        location = r.find("span", class_="content__3ZUKJ clamp-content").text
        Filter_Jobs({
            "timestamp": post_date,
            "title": position,
            "company": company_name,
            "company_logo": "https://www.citypng.com/public/uploads/preview/tiktok-circle-round-logo-brand-video-tik-tok-11583757667gwiiaepkzu.png",
            "url": apply_url,
            "location": location,
            "source": company_name,
            "source_url": "https://careers.tiktok.com/"
        })


def get_url():
    page = 1
    while page < 4:
        try:
            url = f"https://careers.tiktok.com/position?keywords=&category=6704215862603155720%2C6850051244971526414%2C6704215901438216462%2C6704215864629004552%2C6704215913488451847&location=&project=&type=&job_hot_flag=&current={page}&limit=1000&functionCategory="
            browser.get(url)
            wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[@class='positionItem__1giWi positionItem']")))
            response = browser.find_element_by_xpath(
                "//html").get_attribute("outerHTML")
            get_results(response)
            page += 1
            time.sleep(10)
        except:
            print(f"=> Failed to scrape TikTok for page {page}")
    browser.quit()


def main():
    get_url()


# main()
# sys.exit(0)
