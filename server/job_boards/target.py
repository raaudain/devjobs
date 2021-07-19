from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests, sys, json, re
from .modules import create_temp_json
# import modules.create_temp_json as create_temp_json


data = create_temp_json.data

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
        "source_url": "https://jobs.target.com/",
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
        position = str(i.find("h2")).replace("<h2>", "").replace("</h2>", "").strip()
        locations_string = str(i.find("span", class_="job-location")).replace('<span class="job-location">', "").replace("</span>", "").strip()
        
        getJobs(date, apply_url, company_name, position, locations_string)


def getURL():
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0"}

    url = f"https://jobs.target.com/search-jobs/results?ActiveFacetID=0&CurrentPage=1&RecordsPerPage=500&Distance=50&RadiusUnitType=0&Keywords=&Location=&ShowRadius=False&IsPagination=False&CustomFacetName=&FacetTerm=&FacetType=0&FacetFilters%5B0%5D.ID=67611&FacetFilters%5B0%5D.FacetType=1&FacetFilters%5B0%5D.Count=232&FacetFilters%5B0%5D.Display=Technology+and+Data+Sciences&FacetFilters%5B0%5D.IsApplied=true&FacetFilters%5B0%5D.FieldName=&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=0&SortDirection=0&SearchType=6&PostalCode=&fc=&fl=&fcf=&afc=&afl=&afcf="

    response = requests.get(url, headers=headers).text
    data = json.loads(response)

    getResults(data)
    # print(data)

def main():
    getURL()

# main()
# sys.exit(0)