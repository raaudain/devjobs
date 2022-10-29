from bs4 import BeautifulSoup
from datetime import datetime
import sys
import json
from selenium import webdriver
from .helpers import create_temp_json
from .helpers import driver
from .helpers.classes import FilterJobs
# import modules.create_temp_json as create_temp_json
# import modules.driver as driver


driver = driver.chrome
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
browser = webdriver.Chrome(executable_path=driver, options=options)


def get_results(item: str):
    data = item["results"]
    soup = BeautifulSoup(data, "lxml")
    results = soup.find_all("li")
    for i in results:
        if i.find("a"):
            date = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
            post_date = datetime.timestamp(
                datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))
            apply_url = f"https://jobs.target.com{i.find('a')['href'].strip()}"
            company_name = "Target"
            position = str(i.find("h2")).replace("<h2>", "").replace(
                "</h2>", "").replace("&amp;", "&").strip()
            location = str(i.find("span", class_="job-location")).replace(
                '<span class="job-location">', "").replace("</span>", "").strip()
            if "None" not in position:
                FilterJobs({
                    "timestamp": post_date,
                    "title": position,
                    "company": company_name,
                    "company_logo": "https://cblproperty.blob.core.windows.net/production/assets/blt4bbf1ac71c3fdb0e-Target_2544.png",
                    "url": apply_url,
                    "location": location,
                    "source": company_name,
                    "source_url": "https://corporate.target.com/careers/corporate"
                })


def get_url():
    try:
        # Add "view-source:" in front of url to avoid Firefox autoformatting for json
        url = "https://jobs.target.com/search-jobs/results?ActiveFacetID=0&CurrentPage=1&RecordsPerPage=500&Distance=50&RadiusUnitType=0&Keywords=&Location=&ShowRadius=False&IsPagination=False&CustomFacetName=&FacetTerm=&FacetType=0&FacetFilters%5B0%5D.ID=67611&FacetFilters%5B0%5D.FacetType=1&FacetFilters%5B0%5D.Count=232&FacetFilters%5B0%5D.Display=Technology+and+Data+Sciences&FacetFilters%5B0%5D.IsApplied=true&FacetFilters%5B0%5D.FieldName=&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=0&SortDirection=0&SearchType=6&PostalCode=&fc=&fl=&fcf=&afc=&afl=&afcf="
        browser.get(url)
        response = browser.find_element_by_tag_name("pre").text
        data = json.loads(response)
        browser.quit()
        get_results(data)
    except:
        print("Error for Target")


def main():
    get_url()


# main()
# sys.exit(0)
