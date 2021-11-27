from bs4 import BeautifulSoup
from datetime import datetime
import sys, json
from selenium import webdriver
from .modules import create_temp_json
from .modules import driver
# import modules.create_temp_json as create_temp_json
# import modules.driver as driver


driver = driver.firefox
options = webdriver.FirefoxOptions()
options.add_argument("--headless")
browser = webdriver.Firefox(executable_path=driver, options=options)


def get_jobs(date: str, apply_url: str, company_name: str, position: str, locations_string: str):
    data = create_temp_json.data
    scraped = create_temp_json.scraped

    postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))

    data.append({
        "timestamp": postDate,
        "title": position,
        "company": company_name,
        "url": apply_url,
        "location": locations_string,
        "source": company_name,
        "source_url": "https://corporate.target.com/careers/corporate",
        "category": "job"
    })
    scraped.add(company_name)
    print(f"=> target: Added {position}")


def get_results(item: str):
    data = item["results"]
    soup = BeautifulSoup(data, "lxml")
    results = soup.find_all("li")

    for i in results:
        if i.find("a"):
            date = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
            apply_url = f"https://jobs.target.com{i.find('a')['href'].strip()}"
            company_name = "Target"
            position = str(i.find("h2")).replace("<h2>", "").replace("</h2>", "").replace("&amp;", "&").strip()
            locations_string = str(i.find("span", class_="job-location")).replace('<span class="job-location">', "").replace("</span>", "").strip()

            if "None" not in position: 
                get_jobs(date, apply_url, company_name, position, locations_string)


def get_url():
    # Add "view-source:" in front of url to avoid firefox autoformatting for json
    url = "view-source:https://jobs.target.com/search-jobs/results?ActiveFacetID=0&CurrentPage=1&RecordsPerPage=500&Distance=50&RadiusUnitType=0&Keywords=&Location=&ShowRadius=False&IsPagination=False&CustomFacetName=&FacetTerm=&FacetType=0&FacetFilters%5B0%5D.ID=67611&FacetFilters%5B0%5D.FacetType=1&FacetFilters%5B0%5D.Count=232&FacetFilters%5B0%5D.Display=Technology+and+Data+Sciences&FacetFilters%5B0%5D.IsApplied=true&FacetFilters%5B0%5D.FieldName=&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=0&SortDirection=0&SearchType=6&PostalCode=&fc=&fl=&fcf=&afc=&afl=&afcf="

    browser.get(url)
    response = browser.find_element_by_tag_name("pre").text
    data = json.loads(response)
    browser.quit()
    get_results(data)


def main():
    get_url()


# main()
# sys.exit(0)