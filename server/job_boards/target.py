from bs4 import BeautifulSoup
from datetime import datetime
import sys, json
from selenium import webdriver
from .modules import create_temp_json
from .modules import driver
# import modules.create_temp_json as create_temp_json
# import modules.driver as driver


driver = driver.firefox

data = create_temp_json.data

options = webdriver.FirefoxOptions()
options.add_argument("--headless")
browser = webdriver.Firefox(executable_path=driver, options=options)


def getJobs(date, apply_url, company_name, position, locations_string):
    date = date
    title = position
    company = company_name
    url = apply_url
    location = locations_string

    # print(date, title, company, url, location)
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
    data = item["results"]
    soup = BeautifulSoup(data, "lxml")
    results = soup.find_all("li")

    for i in results:
        date = datetime.strftime(datetime.now(), "%Y-%m-%d")
        apply_url = f"https://jobs.target.com{i.find('a')['href'].strip()}"
        company_name = "Target"
        position = str(i.find("h2")).replace("<h2>", "").replace("</h2>", "").replace("&amp;", "&").strip()
        locations_string = str(i.find("span", class_="job-location")).replace('<span class="job-location">', "").replace("</span>", "").strip()
        
        if position != "None" or position != None:
            getJobs(date, apply_url, company_name, position, locations_string)


def getURL():
    # Add "view-source:" in front of url to avoid firefox autoformatting for json
    url = "view-source:https://jobs.target.com/search-jobs/results?ActiveFacetID=0&CurrentPage=1&RecordsPerPage=500&Distance=50&RadiusUnitType=0&Keywords=&Location=&ShowRadius=False&IsPagination=False&CustomFacetName=&FacetTerm=&FacetType=0&FacetFilters%5B0%5D.ID=67611&FacetFilters%5B0%5D.FacetType=1&FacetFilters%5B0%5D.Count=232&FacetFilters%5B0%5D.Display=Technology+and+Data+Sciences&FacetFilters%5B0%5D.IsApplied=true&FacetFilters%5B0%5D.FieldName=&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=0&SortDirection=0&SearchType=6&PostalCode=&fc=&fl=&fcf=&afc=&afl=&afcf="

    browser.get(url)

    response = browser.find_element_by_tag_name("pre").text

    data = json.loads(response)
    browser.quit()

    getResults(data)


    # print(data)

def main():
    getURL()

# main()
# sys.exit(0)