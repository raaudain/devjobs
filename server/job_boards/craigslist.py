from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests, sys, json, time, re, random
from .modules import headers as h
from .modules import create_temp_json
# import modules.headers as h
# import modules.create_temp_json as create_temp_json

f = open(f"./data/params/us_and_ca.txt", "r")
locations = [location.strip() for location in f]
f.close()

m = open(f"./data/params/miami.txt", "r")
miamis = [miami.strip() for miami in m]
m.close()

scraped = create_temp_json.scraped
data = create_temp_json.data




def getJobs(item, location):
    for job in item:
        date = job.find("time", {"class": "result-date"})["datetime"]
        title = job.find("a", {"class": "result-title hdrlnk"}).text
        url = job.find("a", href=True)["href"]
        # location = re.search(r"https://(.*?).craigslist.org", url).group(1)
        location = location.strip()

        age = datetime.timestamp(datetime.now() - timedelta(days=14))
        postDate = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d %H:%M"))

        if url not in scraped and age <= postDate:
            data.append({
                "timestamp": postDate,
                "title": title,
                "company": None,
                "url": url,
                "location": location,
                "source": "Craigslist",
                "source_url": "https://www.craigslist.org",
                "category": "job"
            })
            scraped.add(url)
            print(f"=> craigslist: Added {title} for {location}")
        else:
            print(f"=> craigslist: Already scraped or too old: {title} for {location}")
        


def getResults(item, city):
    cities = {
        "auburn":"AL",
        "bham":"AL",
        "dothan":"AL",
        "shoals":"AL",
        "mobile":"AL",
        "montgomery":"AL",
        "tuscaloosa":"AL",
        "anchorage":"AK",
        "fairbanks":"AK",
        "kenai":"AK",
        "juneau":"AK",
        "flagstaff":"AZ",
        "phoenix":"AZ",
        "yuma":"AZ",
        "fayar":"AR",
        "jonesboro":"AR",
        "texarkana":"AR",
        "bakersfield":"CA",
        "chico":"CA",
        "hanford":"CA",
        "humboldt":"CA",
        "losangeles":"CA",
        "merced":"CA",
        "redding":"CA",
        "sandiego":"CA",
        "sfbay":"CA",
        "slo":"CA",
        "santabarbara":"CA",
        "santamaria":"CA",
        "siskiyou":"CA",
        "susanville":"CA",
        "boulder":"CO",
        "denver":"CO",
        "eastco":"CO",
        "newlondon":"CT",
        "newhaven":"CT",
        "daytona":"FL",
        "keys":"FL",
        "fortlauderdale":"FL",
        "fortmyers":"FL",
        "jacksonville":"FL",
        "orlando":"FL",
        "panamacity":"FL",
        "pensacola":"FL",
        "staugustine":"FL",
        "tallahassee":"FL",
        "treasure":"FL",
        "albanyga":"GA",
        "atlanta":"GA",
        "augusta":"GA",
        "brunswick":"GA",
        "macon":"GA",
        "savannah":"GA",
        "statesboro":"GA",
        "valdosta":"GA",
        "honolulu":"HI",
        "boise":"ID",
        "eastidaho":"ID",
        "lewiston":"ID",
        "twinfalls":"ID",
        "bn":"IL",
        "chicago":"IL",
        "decatur":"IL",
        "carbondale":"IL",
        "bloomington":"IN",
        "evansville":"IN",
        "fortwayne":"IN",
        "indianapolis":"IN",
        "kokomo":"IN",
        "richmondin":"IN",
        "terrehaute":"IN",
        "ames":"IA",
        "cedarrapids":"IA",
        "desmoines":"IA",
        "dubuque":"IA",
        "fortdodge":"IA",
        "iowacity":"IA",
        "masoncity":"IA",
        "quadcities":"IA",
        "siouxcity":"IA",
        "ottumwa":"IA",
        "waterloo":"IA",
        "lawrence":"KS",
        "nwks":"KS",
        "salina":"KS",
        "seks":"KS",
        "swks":"KS",
        "topeka":"KS",
        "wichita":"KS",
        "eastky":"KY",
        "owensboro":"KY",
        "westky":"KY",
        "batonrouge":"LA",
        "cenla":"LA",
        "houma":"LA",
        "lakecharles":"LA",
        "monroe":"LA",
        "neworleans":"LA",
        "shreveport":"LA",
        "baltimore":"MD",
        "westmd":"MD",
        "boston":"MA",
        "capecod":"MA",
        "annarbor":"MI",
        "battlecreek":"MI",
        "centralmich":"MI",
        "detroit":"MI",
        "flint":"MI",
        "grandrapids":"MI",
        "holland":"MI",
        "kalamazoo":"MI",
        "lansing":"MI",
        "monroemi":"MI",
        "muskegon":"MI",
        "nmi":"MI",
        "porthuron":"MI",
        "saginaw":"MI",
        "swmi":"MI",
        "thumb":"MI",
        "up":"MI",
        # bemidji
        # brainerd
        # duluth
        # mankato
        # minneapolis
        # rmn
        # marshall
        # stcloud
        # gulfport
        # hattiesburg
        # jackson
        # meridian
        # northmiss
        # natchez
        # columbiamo
        # joplin
        # kansascity
        # kirksville
        # loz
        # semo
        # springfield
        # stjoseph
        # stlouis
        # billings
        # bozeman
        # butte
        # greatfalls
        # helena
        # kalispell
        # missoula
        # montana
        # grandisland
        # lincoln
        # northplatte
        # omaha
        # scottsbluff
        # elko
        # lasvegas
        # reno
        # nh
        # cnj
        # jerseyshore
        # newjersey
        # southjersey
        # albuquerque
        # clovis
        # farmington
        # lascruces
        # roswell
        # santafe
        # albany
        # binghamton
        # buffalo
        # catskills
        # chautauqua
        # elmira
        # fingerlakes
        # glensfalls
        # hudsonvalley
        # ithaca
        # longisland
        # newyork
        # oneonta
        # plattsburgh
        # potsdam
        # rochester
        # syracuse
        # twintiers
        # utica
        # watertown
        # asheville
        # boone
        # charlotte
        # eastnc
        # fayetteville
        # greensboro
        # hickory
        # onslow
        # outerbanks
        # raleigh
        # wilmington
        # winstonsalem
        # bismarck
        # fargo
        # grandforks
        # nd
        # akroncanton
        # ashtabula
        # athensohio
        # chillicothe
        # cincinnati
        # cleveland
        # columbus
        # dayton
        # limaohio
        # mansfield
        # sandusky
        # toledo
        # tuscarawas
        # youngstown
        # zanesville
        # lawton
        # enid
        # oklahomacity
        # stillwater
        # tulsa
        # bend
        # corvallis
        # eastoregon
        # eugene
        # klamath
        # medford
        # oregoncoast
        # portland
        # roseburg
        # salem
        # altoona
        # chambersburg
        # erie
        # harrisburg
        # lancaster
        # allentown
        # meadville
        # philadelphia
        # pittsburgh
        # poconos
        # reading
        # scranton
        # pennstate
        # williamsport
        # york
        # providence
        # charleston
        # columbia
        # florencesc
        # greenville
        # hiltonhead
        # myrtlebeach
        # nesd
        # csd
        # rapidcity
        # siouxfalls
        # sd
        # chattanooga
        # clarksville
        # jacksontn
        # knoxville
        # memphis
        # nashville
        # tricities
        # abilene
        # amarillo
        # austin
        # beaumont
        # dallas
        # nacogdoches
        # elpaso
        # galveston
        # houston
        # lubbock
        # mcallen
        # odessa
        # sanangelo
        # sanantonio
        # waco
        # wichitafalls
        # logan
        # ogden
        # provo
        # saltlakecity
        # stgeorge
        # vermont
        # norfolk
        # harrisonburg
        # lynchburg
        # blacksburg
        # richmond
        # roanoke
        # swva
        # olympic
        # pullman
        # seattle
        # spokane
        # charlestonwv
        # martinsburg
        # huntington
        # morgantown
        # wheeling
        # parkersburg
        # swv
        # wv
        # appleton
        # eauclaire
        # greenbay
        # lacrosse
        # madison
        # milwaukee
        # northernwi
        # sheboygan
        # wausau
        # wyoming
        # micronesia
        # puertorico
        # virgin
        # calgary
        # edmonton
        # ftmcmurray
        # lethbridge
        # hat
        # peace
        # reddeer
        # cariboo
        # comoxvalley
        # princegeorge
        # skeena
        # vancouver
        # winnipeg
        # newbrunswick
        # newfoundland
        # territories
        # yellowknife
        # halifax
        # barrie
        # belleville
        # chatham
        # londonon
        # niagara
        # ottawa
        # sarnia
        # soo
        # sudbury
        # thunderbay
        # toronto
        # windsor
        # montreal
        # quebec
        # saguenay
        # regina
        # saskatoon
        # whitehorse
        "http://miami.craigslist.org/brw/":"FL",
        "http://miami.craigslist.org/mdc/":"FL",
        "https://miami.craigslist.org/":"FL",
        "http://miami.craigslist.org/pbc/":"FL",
    }

    soup = BeautifulSoup(item, "lxml")
    place = soup.find("title").text.replace(" technical support jobs - craigslist", "").replace(" software/qa/dba/etc jobs - craigslist", "").split(" ")
    location = ""

    for i in place:
        if len(place) > 1:
            # This is to avoid messing with state abbriviation capitalization
            if len(i) > 2:
                location += i.capitalize()+" "
            else:
                location += i+" "
        else:
            location = f"{i.capitalize()}, {cities[city]}"

    location = f"{location.strip()}, {cities[city]}" if cities[city] not in location else location

    results = soup.find_all("div", {"class": "result-info"})

    # print(location, place)
    getJobs(results, location)

def getURL(items):
    count = 1

    for location in items:
        try:
            headers = {"User-Agent": random.choice(h.headers)}
            url = f"https://{location}.craigslist.org/search/sof?lang=en"
            response = requests.get(url, headers=headers)

            if response.ok:
                getResults(response.text, location)
            else:
                print(f"Error for {location}: {response.status_code}")

            if count % 10 == 0:
                time.sleep(5)
            
            count += 1
        except:
            print(f"=> craigslist: Failed to scrape {location}. Continue to next")
            continue

def getURLMiami(items):
    count = 1

    for location in items:
        try:
            headers = {"User-Agent": random.choice(h.headers)}
            url = f"{location}d/software-qa-dba-etc/search/mdc/sof?lang=en"
            response = requests.get(url, headers=headers)

            if response.ok:
                getResults(response.text, location)
            else:
                print(f"Error for {location}: {response.status_code}")

            if count % 10 == 0:
                time.sleep(5)
            
            count += 1
        except:
            print(f"=> craigslist: Failed to scrape {location}. Going to next.")
            continue

def getURL_IT(items):
    count = 1

    for location in items:
        try:
            headers = {"User-Agent": random.choice(h.headers)}
            url = f"https://{location}.craigslist.org/search/tch?lang=en"
            response = requests.get(url, headers=headers)

            if response.ok:
                getResults(response.text, location)
            else:
                print(f"Error: {response.status_code}")

            if count % 10 == 0:
                time.sleep(5)
            
            count += 1
        except:
            print(f"=> craigslist: Failed to scrape {location}. Continue to next")
            continue

def getURLMiami_IT(items):
    count = 1

    for location in items:
        try:
            headers = {"User-Agent": random.choice(h.headers)}
            url = f"{location}d/technical-support/search/mdc/tch?lang=en"
            response = requests.get(url, headers=headers)

            if response.ok:
                getResults(response.text, location)
            else:
                print(f"Error: {response.status_code}")

            if count % 10 == 0:
                time.sleep(5)
            
            count += 1
        except:
            print(f"=> craigslist: Failed to scrape {location}. Going to next.")
            continue

def main():
    getURL(locations)
    getURLMiami(miamis)
    getURL_IT(locations)
    getURLMiami_IT(miamis)

# main()

# sys.exit(0)