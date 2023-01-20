from bs4 import BeautifulSoup
from datetime import datetime
import sys
import json
from playwright.sync_api import sync_playwright
sys.path.insert(0, ".")
from server.job_boards.helpers.classes import ProcessCompanyJobData


process_data = ProcessCompanyJobData()


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
                process_data.filter_jobs({
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

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url)
            response = page.inner_text("pre")

            data = json.loads(response)
            get_results(data)
    except Exception as e:
        print("Error for Target:", e)


def main():
    get_url()


if __name__ == "__main__":
    main()
