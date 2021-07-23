from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests, sys, json, re
# from .modules import create_temp_json
import modules.create_temp_json as create_temp_json


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
    header1 = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }

    session = requests.Session()

    tokens = session.get("https://www.target.com/", headers=header1).cookies.get_dict()

    print(tokens)

    tealeafAkaSid = tokens['TealeafAkaSid']
    sapphire = tokens['sapphire']
    visitorId = tokens['visitorId']
    guestLocation = tokens['GuestLocation']
    webuiVisitorStatus = tokens['webuiVisitorStatus']

    # print(tealeafAkaSid, sapphire, visitorId, guestLocation, webuiVisitorStatus)

    url = f"https://jobs.target.com/search-jobs/results?ActiveFacetID=0&CurrentPage=1&RecordsPerPage=500&Distance=50&RadiusUnitType=0&Keywords=&Location=&ShowRadius=False&IsPagination=False&CustomFacetName=&FacetTerm=&FacetType=0&FacetFilters%5B0%5D.ID=67611&FacetFilters%5B0%5D.FacetType=1&FacetFilters%5B0%5D.Count=232&FacetFilters%5B0%5D.Display=Technology+and+Data+Sciences&FacetFilters%5B0%5D.IsApplied=true&FacetFilters%5B0%5D.FieldName=&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=0&SortDirection=0&SearchType=6&PostalCode=&fc=&fl=&fcf=&afc=&afl=&afcf="


    header2 = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Cookie":f"TealeafAkaSid={tealeafAkaSid}; sapphire={sapphire}; visitorId:{visitorId}; GuestLocation={guestLocation}; "
    }

    payload = {
        "grant_type":"refresh_token",
        "client_credential":{
            "client_id":"ecom-web-1.0.0"
        },
        "device_info":{
            "user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "language":"en-US","color_depth":"30","device_memory":"8","pixel_ratio":"unknown",
            "hardware_concurrency":"8","resolution":"[1680,1050]","available_resolution":"[1680,967]","timezone_offset":"420","session_storage":"1",
            "local_storage":"1",
            "indexed_db":"1",
            "add_behavior":"unknown",
            "open_database":"1",
            "cpu_class":"unknown",
            "navigator_platform":"MacIntel",
            "do_not_track":"unknown",
            "regular_plugins":"[\"Chromium PDF Plugin::Portable Document Format::application/x-google-chrome-pdf~pdf\",\"Chromium PDF Viewer::::application/pdf~pdf\"]",
            "adblock":"false",
            "has_lied_languages":"false",
            "has_lied_resolution":"false",
            "has_lied_os":"true",
            "has_lied_browser":"false",
            "touch_support":"[0,false,false]",
            "js_fonts":"[\"Andale Mono\",\"Arial\",\"Arial Black\",\"Arial Hebrew\",\"Arial Narrow\",\"Arial Rounded MT Bold\",\"Arial Unicode MS\",\"Calibri\",\"Comic Sans MS\",\"Courier\",\"Courier New\",\"Geneva\",\"Georgia\",\"Helvetica\",\"Helvetica Neue\",\"Impact\",\"LUCIDA GRANDE\",\"Microsoft Sans Serif\",\"Monaco\",\"MYRIAD PRO\",\"Palatino\",\"Tahoma\",\"Times\",\"Times New Roman\",\"Trebuchet MS\",\"Verdana\",\"Wingdings\",\"Wingdings 2\",\"Wingdings 3\"]",
            "navigator_vendor":"Google Inc.",
            "navigator_app_name":"Netscape","navigator_app_code_name":"Mozilla",
            "navigator_app_version":"5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "navigator_languages":"[\"en-US\",\"en\"]","navigator_cookies_enabled":"true","navigator_java_enabled":"false","visitor_id":f"{visitorId}",
            "tealeaf_id":f"{tealeafAkaSid}",
            "webgl_vendor":"Google Inc. (ATI Technologies Inc.)~ANGLE (ATI Technologies Inc., AMD Radeon Pro 555 OpenGL Engine, OpenGL 4.1 ATI-4.5.14)",
            "browser_name":"Chrome",
            "browser_version":"91.0.4472.124",
            "cpu_architecture":"amd64","device_vendor":"Unknown","device_model":"Unknown",
            "device_type":"Unknown",
            "engine_name":"Blink",
            "engine_version":"91.0.4472.124",
            "os_name":"Windows",
            "os_version":"10"
        }
    }

    access = requests.post("https://gsp.target.com/gsp/oauth_tokens/v2/client_tokens", json=payload, headers=header2).cookies.get_dict()

    accessToken = access["accessToken"]
    egsSessionId = access["egsSessionId"]
    idToken = access["idToken"]
    refreshToken = access["refreshToken"]

    header3 = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Cookie":f"TealeafAkaSid={tealeafAkaSid}; sapphire={sapphire}; visitorId:{visitorId}; GuestLocation={guestLocation}; webuiVisitorStatus={webuiVisitorStatus}; accessToken={accessToken}; egsSessionId={egsSessionId}; idToken={idToken}; refreshToken={refreshToken}"
    }

    response = requests.get(url, headers=header3).text
    data = json.loads(response)

    getResults(data)


    # print(data)

def main():
    getURL()

main()
sys.exit(0)