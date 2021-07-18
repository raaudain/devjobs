import requests, sys, re, time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


# driver = r"/usr/local/bin/geckodriver"

# browser = webdriver.Firefox(executable_path=driver)
# wait = WebDriverWait(browser, 120)


# words = "./data/params/workable.txt"
# www = r"https://apply.workable.com/(.*?)/"
# link = "https://apply.workable.com"


# words = "./data/params/greenhouse_io.txt"
# www = r"https://boards.greenhouse.io/(.*?)/"
# link = "https://boards.greenhouse.io"


# words = "./data/params/lever_co.txt"
# www = r"https://jobs.lever.co/(.*?)/"
# link = "https://jobs.lever.co"

# words = "./data/params/smartrecruiters.txt"
# www = r"https://careers.smartrecruiters.com/(.*?)/"
# link = "https://careers.smartrecruiters.com"

# words = "./data/params/ashbyhq.txt"
# www = r"https://jobs.ashbyhq.com/(.*?)/"
# link = "https://jobs.ashbyhq.com"

words = "./data/params/jazzhr.txt"
www = r"https://(.*?).applytojob.com/"
link = "https://jobs.ashbyhq.com"


f = open(words, "r")
text = [company.lower().strip() for company in f]
f.close()


duck = [
  "https://kbs.applytojob.com/",
  "https://enerjet.applytojob.com/",
  "https://risemodular.applytojob.com/",
  "https://affinitygroup.applytojob.com/",
  "https://crownacehardware.applytojob.com/",
  "https://gulftechintl.applytojob.com/",
  "https://hubner.applytojob.com/",
  "https://circlelinkhealth.applytojob.com/",
  "https://quickquackcarwash.applytojob.com/",
  "https://ymcaofgreaterfortwayne.applytojob.com/",
  "https://nro.applytojob.com/",
  "https://goldencustomercare.applytojob.com/",
  "https://sanfordfederal.applytojob.com/",
  "https://leaprecruit.applytojob.com/",
  "https://zeroavia.applytojob.com/",
  "https://perchhq.applytojob.com/",
  "https://fargov.applytojob.com/",
  "https://akebonobrakecorporation.applytojob.com/",
  "https://districtphoto.applytojob.com/",
  "https://gulfstreamgoodwill.applytojob.com/",
  "https://studygroupuk.applytojob.com/",
  "https://uptoparservicesllc.applytojob.com/",
  "https://ubiquity.applytojob.com/",
  "https://canadianwildlifefederation.applytojob.com/",
  "https://saatva.applytojob.com/",
  "https://thedelanoymanagementgroup.applytojob.com/",
  "https://cmt.applytojob.com/",
  "https://sacramentocreditunion.applytojob.com/",
  "https://wspartnersofga.applytojob.com/",
  "https://starsandstrikes.applytojob.com/",
  "https://advancednutrients.applytojob.com/",
  "https://crownacehardware.applytojob.com/",
  "https://kestrafinancial.applytojob.com/",
  "https://nro.applytojob.com/",
  "https://masglobalconsulting.applytojob.com/",
  "https://spiritstaffingandconsultinginc.applytojob.com/",
  "https://oklahomadepartmentofhumanservices.applytojob.com/",
  "https://excellenceservices.applytojob.com/",
  "https://pbssystems.applytojob.com/",
  "https://ambatovy.applytojob.com/",
  "https://imperativecare.applytojob.com/",
  "https://theemersonmanagementgroup.applytojob.com/",
  "https://heritage.applytojob.com/",
  "https://expertiselocal.applytojob.com/",
  "https://versatile.applytojob.com/",
  "https://akebonobrakecorporation.applytojob.com/",
  "https://jacksonservicesinc.applytojob.com/",
  "https://aaaaerospaceusainc.applytojob.com/",
  "https://starsandstrikes.applytojob.com/",
  "https://kenson.applytojob.com/",
  "https://woodgreencommunityservices.applytojob.com/",
  "https://centrumvalleyfarms.applytojob.com/",
  "https://quickquackcarwash.applytojob.com/",
  "https://gulfstreamgoodwill.applytojob.com/",
  "https://oakfort.applytojob.com/",
  "https://voloteacabincrew.applytojob.com/",
  "https://ctstatecommunitycollege.applytojob.com/",
  "https://principlechoicesolutions.applytojob.com/",
  "https://cmt.applytojob.com/",
  "https://luxfermagtech.applytojob.com/",
  "https://interac.applytojob.com/",
  "https://eaglesg.applytojob.com/",
  "https://cloudmed.applytojob.com/",
  "https://entravision.applytojob.com/",
  "https://bothouniversity.applytojob.com/",
  "https://phalenleadershipacademies.applytojob.com/",
  "https://holtecmfg.applytojob.com/",
  "https://24hrsafetyllc.applytojob.com/",
  "https://everythingbutthehouse.applytojob.com/",
  "https://childandfamily.applytojob.com/",
  "https://zermountinc.applytojob.com/",
  "https://macphailcenterformusic.applytojob.com/",
  "https://performancesearchgroup.applytojob.com/",
  "https://nrtc.applytojob.com/",
  "https://screenrant.applytojob.com/",
  "https://densfs.applytojob.com/",
  "https://springbox.applytojob.com/",
  "https://plattcollegelosangelesllc.applytojob.com/",
  "https://centerforglobaldevelopment.applytojob.com/apply/QVD4m7WNtX/Research-AssistantProgramme-Coordinator-UK",
  "https://nro.applytojob.com/apply/LZomxy5RBO/Summer-2022-NRO-Cadre-Student-Internship-Program",
  "https://entravision.applytojob.com/",
  "https://imanagecom.applytojob.com/",
  "https://selectra.applytojob.com/",
  "https://medirevv.applytojob.com/",
  "https://rhythmpharmaceuticals.applytojob.com/",
  "https://govhrusa.applytojob.com/",
  "https://samasource.applytojob.com/",
  "https://krystalbiotech.applytojob.com/",
  "https://abimarfoods.applytojob.com/",
  "https://sacramentocreditunion.applytojob.com/",
  "https://ejam.applytojob.com/",
  "https://lastmilehealth.applytojob.com/",
  "https://voloteacabincrew.applytojob.com/apply/uATQD8e4xJ/Cabin-Crew-With-Cabin-Crew-Attestation",
  "https://flossbar.applytojob.com/",
  "https://maple.applytojob.com/",
  "https://maacproject.applytojob.com/",
  "https://routeware.applytojob.com/",
  "https://partnerhero.applytojob.com/",
  "https://medlineca.applytojob.com/",
  "https://nes.applytojob.com/",
  "https://onehope.applytojob.com/",
  "https://nationalhealthtransport.applytojob.com/",
  "https://odmhsas.applytojob.com/",
  "https://shorelinewestregion.applytojob.com/",
  "https://wonderlicinc.applytojob.com/",
  "https://vodeno.applytojob.com/",
  "https://happydaytransit.applytojob.com/",
  "https://restore.applytojob.com/",
  "https://theoutreachteam.applytojob.com/",
  "https://beemaclogistics.applytojob.com/",
  "https://covenanthouse.applytojob.com/",
  "https://wonderdynamics.applytojob.com/",
  "https://caineweiner.applytojob.com/",
  "https://dlocal.applytojob.com/",
  "https://servbehavioralhealthsystem.applytojob.com/",
  "https://bostonglobemediapartners.applytojob.com/",
  "https://meriplexcommunications.applytojob.com/",
  "https://heartandstroke.applytojob.com/",
  "https://fwf.applytojob.com/",
  "https://blusharkdigital.applytojob.com/",
  "https://perscholasinc.applytojob.com/",
  "https://dowbuilt.applytojob.com/",
  "https://bankofjamaica.applytojob.com/",
  "https://moonlightcompanies.applytojob.com/",
  "https://montanatechuniversity.applytojob.com/",
  "https://proactivemd.applytojob.com/",
  "https://epworthvilla.applytojob.com/apply",
  "https://agatlaboratories.applytojob.com/",
  "https://comicbookresourcescbr.applytojob.com/",
  "https://butler.applytojob.com/",
  "https://savilinx.applytojob.com/",
  "https://aamco.applytojob.com/",
  "https://stillwater.applytojob.com/",
  "https://wnaltdcom.applytojob.com/",
  "https://habasitamerica.applytojob.com/",
  "https://immaculateflight.applytojob.com/",
  "https://odmhsas.applytojob.com/",
  "https://sparrowliving.applytojob.com/",
  "https://propercannabis.applytojob.com/",
  "https://elginfasteners.applytojob.com/",
  "https://rembrandtfoods.applytojob.com/",
  "https://exzeons.applytojob.com/",
  "https://franklinpierceuniversity.applytojob.com/",
  "https://smartco.applytojob.com/",
  "https://onerail.applytojob.com/",
  "https://universityofmary.applytojob.com/",
  "https://tachus.applytojob.com/",
  "https://mmihospitality.applytojob.com/",
  "https://enkoeducation.applytojob.com/",
  "https://crownhealth.applytojob.com/",
  "https://northwestregion.applytojob.com/",
  "https://gellertglobalgroup.applytojob.com/",
  "https://reformalliance.applytojob.com/",
  "https://frionaindustries.applytojob.com/",
  "https://betterearth.applytojob.com/",
  "https://westcoastpavingstones.applytojob.com/",
  "https://communityhumanservices.applytojob.com/",
  "https://ams.applytojob.com/",
  "https://highflyingfoods.applytojob.com/",
  "https://cloudcmllc.applytojob.com/",
  "https://tempusinc.applytojob.com/",
  "https://famous.applytojob.com/",
  "https://ophthalmicconsultantsofbostoninc.applytojob.com/",
  "https://ilabank.applytojob.com/",
  "https://novapioneer.applytojob.com/",
  "https://courthousefitness.applytojob.com/",
  "https://livinggoods.applytojob.com/",
  "https://santacruzbicycles.applytojob.com/",
  "https://idsinternational.applytojob.com/",
  "https://californiaacademyofsciences.applytojob.com/",
  "https://philamuseum.applytojob.com/",
  "https://mysurestart.applytojob.com/",
  "https://momentumsolar.applytojob.com/",
  "https://forever.applytojob.com/",
  "https://giffords.applytojob.com/",
  "https://nichiha.applytojob.com/",
  "https://talusbio.applytojob.com/",
  "https://taconicbiosciences.applytojob.com/",
  "https://brookfieldam.applytojob.com/apply/IW2xKUGdPk/Analyst-Investments-Renewable-Power",
  "https://recoded.applytojob.com/apply/3pZfxPElEp/Director-Of-Global-Partnerships"
]

w = []
added = set()
for i in duck:
    # print(i)
    word = re.findall(www, i)
    # word = re.findall(r"https://boards.greenhouse.io/(.*?)/", i)
    print(word)
    if word:
        w.append(*word)
        

for c in w:
    d = c.lower()
    if d not in text and d not in added and d != "j":
        a = open(words, "a")
        a.write(f"{c}\n")
        a.close()
        added.add(d)
    

# headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"}

# bypassRecaptcha = "http://webcache.googleusercontent.com/search?q=cache:"

# page = 0

# while page < 1:
#     print("Page", page+1)

#     url = f"https://www.google.com/search?q=site:jobs.lever.co&ei=7nbjYMK6INLb-gTbx4HQBA&start={page}&sa=N&ved=2ahUKEwjC6YSs7czxAhXSrZ4KHdtjAEoQ8tMDegQIARA3&biw=1680&bih=461"

#     browser.get(url)
            
#     wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='pnnext']")))
#             # time.sleep(10)
#     # if wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='pnnext']"))):
#     response = browser.find_element_by_xpath("//*").get_attribute("outerHTML")
    
#     # time.sleep(5)
#     # response = requests.get(url, headers=headers)

#     # if response.ok:
#     soup = BeautifulSoup(response, "lxml")
#     href = soup.find_all("a", href=re.compile(link))
#     # print(href)
#     companies = []
#     added = set()

#     for h in href:
#         r = h["href"]
#         print(r)
#         word = re.findall(www, r)
#         if word: 
#             print("word", word)
#             companies.append(*word)

#     for c in companies:
#         d = c.lower()
#         if d not in text and d not in added and d != "j":
#             a = open(words, "a")
#             a.write(f"{d}\n")
#             a.close()
#             added.add(d)

#             if len(companies) < 1:
#                 break

#         companies = []

#     time.sleep(10)
#     page += 1
    

sys.exit(0)