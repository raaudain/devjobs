import requests
import sys
import time
import random
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from .modules import headers as h
from .modules import create_temp_json
from .modules.classes import Filter_Jobs
# import modules.headers as h
# import modules.create_temp_json as create_temp_json


def get_results(item: str, city: str):
    cities = {
        "auburn": "AL",
        "bham": "AL",
        "dothan": "AL",
        "shoals": "AL",
        "mobile": "AL",
        "montgomery": "AL",
        "tuscaloosa": "AL",
        "anchorage": "AK",
        "fairbanks": "AK",
        "kenai": "AK",
        "juneau": "AK",
        "flagstaff": "AZ",
        "phoenix": "AZ",
        "yuma": "AZ",
        "fayar": "AR",
        "jonesboro": "AR",
        "texarkana": "AR",
        "bakersfield": "CA",
        "chico": "CA",
        "hanford": "CA",
        "humboldt": "CA",
        "losangeles": "CA",
        "merced": "CA",
        "redding": "CA",
        "sandiego": "CA",
        "sfbay": "CA",
        "slo": "CA",
        "santabarbara": "CA",
        "santamaria": "CA",
        "siskiyou": "CA",
        "susanville": "CA",
        "boulder": "CO",
        "denver": "CO",
        "eastco": "CO",
        "newlondon": "CT",
        "newhaven": "CT",
        "daytona": "FL",
        "keys": "FL",
        "fortlauderdale": "FL",
        "fortmyers": "FL",
        "jacksonville": "FL",
        "orlando": "FL",
        "panamacity": "FL",
        "pensacola": "FL",
        "staugustine": "FL",
        "tallahassee": "FL",
        "treasure": "FL",
        "albanyga": "GA",
        "atlanta": "GA",
        "augusta": "GA",
        "brunswick": "GA",
        "macon": "GA",
        "savannah": "GA",
        "statesboro": "GA",
        "valdosta": "GA",
        "honolulu": "HI",
        "boise": "ID",
        "eastidaho": "ID",
        "lewiston": "ID",
        "twinfalls": "ID",
        "bn": "IL",
        "chicago": "IL",
        "decatur": "IL",
        "carbondale": "IL",
        "bloomington": "IN",
        "evansville": "IN",
        "fortwayne": "IN",
        "indianapolis": "IN",
        "kokomo": "IN",
        "richmondin": "IN",
        "terrehaute": "IN",
        "ames": "IA",
        "cedarrapids": "IA",
        "desmoines": "IA",
        "dubuque": "IA",
        "fortdodge": "IA",
        "iowacity": "IA",
        "masoncity": "IA",
        "quadcities": "IA",
        "siouxcity": "IA",
        "ottumwa": "IA",
        "waterloo": "IA",
        "lawrence": "KS",
        "nwks": "KS",
        "salina": "KS",
        "seks": "KS",
        "swks": "KS",
        "topeka": "KS",
        "wichita": "KS",
        "eastky": "KY",
        "owensboro": "KY",
        "westky": "KY",
        "batonrouge": "LA",
        "cenla": "LA",
        "houma": "LA",
        "lakecharles": "LA",
        "monroe": "LA",
        "neworleans": "LA",
        "shreveport": "LA",
        "baltimore": "MD",
        "westmd": "MD",
        "boston": "MA",
        "capecod": "MA",
        "annarbor": "MI",
        "battlecreek": "MI",
        "centralmich": "MI",
        "detroit": "MI",
        "flint": "MI",
        "grandrapids": "MI",
        "holland": "MI",
        "kalamazoo": "MI",
        "lansing": "MI",
        "monroemi": "MI",
        "muskegon": "MI",
        "nmi": "MI",
        "porthuron": "MI",
        "saginaw": "MI",
        "swmi": "MI",
        "thumb": "MI",
        "up": "MI",
        "bemidji": "MN",
        "brainerd": "MN",
        "duluth": "MN",
        "mankato": "MN",
        "minneapolis": "MN",
        "rmn": "MN",
        "marshall": "MN",
        "stcloud": "MN",
        "gulfport": "MS",
        "hattiesburg": "MS",
        "jackson": "MS",
        "meridian": "MS",
        "northmiss": "MS",
        "natchez": "MS",
        "columbiamo": "MO",
        "joplin": "MO",
        "kansascity": "MO",
        "kirksville": "MO",
        "loz": "MO",
        "semo": "MO",
        "springfield": "MO",
        "stjoseph": "MO",
        "stlouis": "MO",
        "billings": "MT",
        "bozeman": "MT",
        "butte": "MT",
        "greatfalls": "MT",
        "helena": "MT",
        "kalispell": "MT",
        "missoula": "MT",
        "montana": "MT",
        "grandisland": "NE",
        "lincoln": "NE",
        "northplatte": "NE",
        "omaha": "NE",
        "scottsbluff": "NE",
        "elko": "NV",
        "lasvegas": "NV",
        "reno": "NV",
        "cnj": "NJ",
        "jerseyshore": "NJ",
        "newjersey": "NJ",
        "southjersey": "NJ",
        "albuquerque": "NM",
        "clovis": "NM",
        "farmington": "NM",
        "lascruces": "NM",
        "roswell": "NM",
        "santafe": "NM",
        "albany": "NY",
        "binghamton": "NY",
        "buffalo": "NY",
        "catskills": "NY",
        "chautauqua": "NY",
        "elmira": "NY",
        "fingerlakes": "NY",
        "glensfalls": "NY",
        "hudsonvalley": "NY",
        "ithaca": "NY",
        "longisland": "NY",
        "newyork": "NY",
        "oneonta": "NY",
        "plattsburgh": "NY",
        "potsdam": "NY",
        "rochester": "NY",
        "syracuse": "NY",
        "twintiers": "NY",
        "utica": "NY",
        "watertown": "NY",
        "asheville": "NC",
        "boone": "NC",
        "charlotte": "NC",
        "eastnc": "NC",
        "fayetteville": "NC",
        "greensboro": "NC",
        "hickory": "NC",
        "onslow": "NC",
        "outerbanks": "NC",
        "raleigh": "NC",
        "wilmington": "NC",
        "winstonsalem": "NC",
        "bismarck": "ND",
        "fargo": "ND",
        "grandforks": "ND",
        "akroncanton": "OH",
        "ashtabula": "OH",
        "athensohio": "OH",
        "chillicothe": "OH",
        "cincinnati": "OH",
        "cleveland": "OH",
        "columbus": "OH",
        "dayton": "OH",
        "limaohio": "OH",
        "mansfield": "OH",
        "sandusky": "OH",
        "toledo": "OH",
        "tuscarawas": "OH",
        "youngstown": "OH",
        "zanesville": "OH",
        "lawton": "OK",
        "enid": "OK",
        "oklahomacity": "OK",
        "stillwater": "OK",
        "tulsa": "OK",
        "bend": "OR",
        "corvallis": "OR",
        "eastoregon": "OR",
        "eugene": "OR",
        "klamath": "OR",
        "medford": "OR",
        "oregoncoast": "OR",
        "portland": "OR",
        "roseburg": "OR",
        "salem": "OR",
        "altoona": "PA",
        "chambersburg": "PA",
        "erie": "PA",
        "harrisburg": "PA",
        "lancaster": "PA",
        "allentown": "PA",
        "meadville": "PA",
        "philadelphia": "PA",
        "pittsburgh": "PA",
        "poconos": "PA",
        "reading": "PA",
        "scranton": "PA",
        "pennstate": "PA",
        "williamsport": "PA",
        "york": "PA",
        "providence": "RI",
        "charleston": "SC",
        "columbia": "SC",
        "florencesc": "SC",
        "greenville": "SC",
        "hiltonhead": "SC",
        "myrtlebeach": "SC",
        "nesd": "SD",
        "csd": "SD",
        "rapidcity": "SD",
        "siouxfalls": "SD",
        "sd": "SD",
        "chattanooga": "TN",
        "clarksville": "TN",
        "jacksontn": "TN",
        "knoxville": "TN",
        "memphis": "TN",
        "nashville": "TN",
        "tricities": "TN",
        "abilene": "TX",
        "amarillo": "TX",
        "austin": "TX",
        "beaumont": "TX",
        "dallas": "TX",
        "nacogdoches": "TX",
        "elpaso": "TX",
        "galveston": "TX",
        "houston": "TX",
        "lubbock": "TX",
        "mcallen": "TX",
        "odessa": "TX",
        "sanangelo": "TX",
        "sanantonio": "TX",
        "waco": "TX",
        "wichitafalls": "TX",
        "logan": "UT",
        "ogden": "UT",
        "provo": "UT",
        "saltlakecity": "UT",
        "stgeorge": "UT",
        "vermont": "VT",
        "norfolk": "VA",
        "harrisonburg": "VA",
        "lynchburg": "VA",
        "blacksburg": "VA",
        "richmond": "VA",
        "roanoke": "VA",
        "swva": "VA",
        "olympic": "WA",
        "pullman": "WA",
        "seattle": "WA",
        "spokane": "WA",
        "charlestonwv": "WV",
        "martinsburg": "WV",
        "huntington": "WV",
        "morgantown": "WV",
        "wheeling": "WV",
        "parkersburg": "WV",
        "swv": "WV",
        "wv": "WV",
        "appleton": "WI",
        "eauclaire": "WI",
        "greenbay": "WI",
        "lacrosse": "WI",
        "madison": "WI",
        "milwaukee": "WI",
        "northernwi": "WI",
        "sheboygan": "WI",
        "wausau": "WI",
        "wyoming": "WY",
        "micronesia": "US",
        "puertorico": "US",
        "virgin": "US",
        "calgary": "AB, Canada",
        "edmonton": "AB, Canada",
        "ftmcmurray": "AB, Canada",
        "lethbridge": "AB, Canada",
        "hat": "AB, Canada",
        "peace": "AB, Canada",
        "reddeer": "AB, Canada",
        "cariboo": "BC, Canada",
        "comoxvalley": "BC, Canada",
        "princegeorge": "BC, Canada",
        "skeena": "BC, Canada",
        "vancouver": "BC, Canada",
        "winnipeg": "MB, Canada",
        "newbrunswick": "NB, Canada",
        "newfoundland": "NL, Canada",
        "territories": "NT, Canada",
        "yellowknife": "NT, Canada",
        "halifax": "NS, Canada",
        "barrie": "ON, Canada",
        "belleville": "ON, Canada",
        "chatham": "ON, Canada",
        "londonon": "ON, Canada",
        "niagara": "ON, Canada",
        "ottawa": "ON, Canada",
        "sarnia": "ON, Canada",
        "soo": "ON, Canada",
        "sudbury": "ON, Canada",
        "thunderbay": "ON, Canada",
        "toronto": "ON, Canada",
        "windsor": "ON, Canada",
        "montreal": "QC, Canada",
        "quebec": "QC, Canada",
        "saguenay": "QC, Canada",
        "regina": "SK, Canada",
        "saskatoon": "SK, Canada",
        "whitehorse": "YT, Canada",
        "http://miami.craigslist.org/brw/": "FL",
        "http://miami.craigslist.org/mdc/": "FL",
        "https://miami.craigslist.org/": "FL",
        "http://miami.craigslist.org/pbc/": "FL",
    }
    soup = BeautifulSoup(item, "lxml")
    place = soup.find("title").text.replace(" technical support jobs - craigslist",
                                            "").replace(" software/qa/dba/etc jobs - craigslist", "").split(" ")
    location = ""
    for i in place:
        if len(place) > 1:
            # This is to avoid messing with state abbriviation capitalization
            if len(i) > 2:
                location += i.capitalize()+" "
            else:
                location += i+" "
        else:
            if city in cities:
                location = f"{i.capitalize()}, {cities[city]}"
    if city in cities:
        if cities[city] not in location:
            location = f"{location.strip()}, {cities[city]}"
        else:
            location = location
    else:
        pass
    results = soup.find_all("div", {"class": "result-info"})
    for job in results:
        date = job.find("time", {"class": "result-date"})["datetime"]
        position = job.find("a", {"class": "result-title hdrlnk"}).text
        apply_url = job.find("a", href=True)["href"]
        location = location.strip()
        age = datetime.timestamp(datetime.now() - timedelta(days=30))
        post_date = datetime.timestamp(
            datetime.strptime(date, "%Y-%m-%d %H:%M"))
        if age <= post_date:
            Filter_Jobs({
                "timestamp": post_date,
                "title": position,
                "company": None,
                "company_logo": "https://logos-world.net/wp-content/uploads/2021/02/Craigslist-Emblem.png",
                "url": apply_url,
                "location": location,
                "source": "Craigslist",
                "source_url": "https://www.craigslist.org"
            })


def get_url(items: list):
    count = 1
    for location in items:
        try:
            headers = {"User-Agent": random.choice(h.headers)}
            url = f"https://{location}.craigslist.org/search/sof?lang=en"
            response = requests.get(url, headers=headers)
            if response.ok:
                get_results(response.text, location)
                if count % 10 == 0:
                    time.sleep(5)
                else:
                    time.sleep(0.05)
            else:
                print(
                    f"=> craigslist: Error for {location}: {response.status_code}")
                break
            count += 1
        except:
            pass


def get_url_miami(items: list):
    count = 1
    for location in items:
        headers = {"User-Agent": random.choice(h.headers)}
        url = f"{location}d/software-qa-dba-etc/search/mdc/sof?lang=en"
        response = requests.get(url, headers=headers)
        if response.ok:
            get_results(response.text, location)
            # if count % 10 == 0: time.sleep(5)
        elif response.status_code == 403 and count < 1:
            print(f"=> craigslist: Sleeping for 15 minutes")
            time.sleep(900)
            count += 1
        else:
            print(
                f"=> craigslist: Error for {location}: {response.status_code}")
            break


def get_url_it(items: list):
    count = 1
    for location in items:
        try:
            headers = {"User-Agent": random.choice(h.headers)}
            url = f"https://{location}.craigslist.org/search/sad?lang=en&cc=gb"
            response = requests.get(url, headers=headers)
            if response.ok:
                get_results(response.text, location)
                if count % 10 == 0:
                    time.sleep(5)
                else:
                    time.sleep(0.05)
            else:
                print(
                    f"=> craigslist: Error for {location}: {response.status_code}")
                break
            count += 1
        except:
            pass


def get_url_miami_it(items: list):
    count = 1
    for location in items:
        headers = {"User-Agent": random.choice(h.headers)}
        url = f"{location}d/technical-support/search/mdc/sad?lang=en&cc=gb"
        response = requests.get(url, headers=headers)
        if response.ok:
            get_results(response.text, location)
            if count % 10 == 0:
                time.sleep(5)
            else:
                time.sleep(0.05)
        else:
            print(
                f"=> craigslist: Error for {location}: {response.status_code}")
            break
        count += 1


def get_url_network(items: list):
    count = 1
    for location in items:
        try:
            headers = {"User-Agent": random.choice(h.headers)}
            url = f"https://{location}.craigslist.org/search/tch?lang=en"
            response = requests.get(url, headers=headers)
            if response.ok:
                get_results(response.text, location)
                if count % 10 == 0:
                    time.sleep(5)
                else:
                    time.sleep(0.05)
            else:
                print(
                    f"=> craigslist: Error for {location}: {response.status_code}")
                break
            count += 1
        except:
            pass


def get_url_web(items: list):
    count = 1
    for location in items:
        try:
            headers = {"User-Agent": random.choice(h.headers)}
            url = f"https://{location}.craigslist.org/search/web?lang=en"
            response = requests.get(url, headers=headers)
            if response.ok:
                get_results(response.text, location)
                if count % 10 == 0:
                    time.sleep(5)
                else:
                    time.sleep(0.05)
            else:
                print(
                    f"=> craigslist: Error for {location}: {response.status_code}")
                break
            count += 1
        except:
            pass


def get_url_miami_network(items: list):
    count = 1
    for location in items:
        try:
            headers = {"User-Agent": random.choice(h.headers)}
            url = f"{location}d/technical-support/search/mdc/tch?lang=en"
            response = requests.get(url, headers=headers)
            if response.ok:
                get_results(response.text, location)
                if count % 10 == 0:
                    time.sleep(5)
                else:
                    time.sleep(0.05)
        except:
            print(
                f"=> craigslist: Error for {location}: {response.status_code}")
        count += 1


def main():
    f = open("./data/params/craigslist.txt", "r")
    locations = [location.strip() for location in f]
    f.close()
    m = open("./data/params/miami.txt", "r")
    miamis = [miami.strip() for miami in m]
    m.close()
    get_url_network(locations)
    get_url_miami_network(miamis)
    get_url(locations)
    get_url_miami(miamis)
    get_url_it(locations)
    get_url_miami_it(miamis)


# main()
# sys.exit(0)
