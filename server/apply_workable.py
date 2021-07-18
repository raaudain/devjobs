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

# words = "./data/params/jazzhr.txt"
# www = r"https://(.*?).applytojob.com/"
# link = "https://jobs.ashbyhq.com"

words = "./data/params/breezyhr.txt"
www = r"https://(.*?).breezy.hr/"
link = "https://jobs.ashbyhq.com"


f = open(words, "r")
text = [company.lower().strip() for company in f]
f.close()


duck = [
  "https://resources.breezy.hr/",
  "https://embraer.breezy.hr/",
  "https://popxo.breezy.hr/",
  "https://canoo.breezy.hr/",
  "https://go2.breezy.hr/p/7d85cd3bcc92-go2-application-form",
  "https://tigo.breezy.hr/p/1f6a25433410-sw-engineer",
  "https://tigo.breezy.hr/p/2088a6418ad9-agente-de-telemarketing",
  "https://spectrumlife.breezy.hr/",
  "https://athena.breezy.hr/",
  "https://getir.breezy.hr/",
  "https://everest.breezy.hr/",
  "https://north-wind-group.breezy.hr/",
  "https://the-hoth.breezy.hr/p/74ad1ef82880",
  "https://sibros.breezy.hr/",
  "https://airband.breezy.hr/",
  "https://domestika.breezy.hr/",
  "https://embryhealth.breezy.hr/",
  "https://commerzbank-poland.breezy.hr/",
  "https://worksmart.breezy.hr/",
  "https://sourcefit-philippines.breezy.hr/",
  "https://scribe.breezy.hr/p/740a946753cf",
  "https://resources.breezy.hr/",
  "https://developer.breezy.hr/",
  "https://acs.breezy.hr/",
  "https://openly.breezy.hr/",
  "https://galvion.breezy.hr/",
  "https://dess.breezy.hr/",
  "https://sibros.breezy.hr/",
  "https://deako.breezy.hr/",
  "https://inspire-hospice-and-palliative-care.breezy.hr/",
  "https://ac-pro.breezy.hr/",
  "https://sourcefit-philippines.breezy.hr/",
  "https://vetsez.breezy.hr/",
  "https://symphony.breezy.hr/",
  "https://mammoth-distribution.breezy.hr/",
  "https://international-automotive-components.breezy.hr/",
  "https://blue-raven-corporate.breezy.hr/",
  "https://family-allergy-asthma.breezy.hr/",
  "https://acs.breezy.hr/",
  "https://galvion.breezy.hr/",
  "https://payspace.breezy.hr/",
  "https://finema.breezy.hr/",
  "https://osmind.breezy.hr/",
  "https://courted.breezy.hr/",
  "https://kitbash3d.breezy.hr/",
  "https://allobee-inc.breezy.hr/",
  "https://novahospitalitycareers.breezy.hr/",
  "https://love-corn.breezy.hr/",
  "https://continued.breezy.hr/",
  "https://openly.breezy.hr/",
  "https://sfr3.breezy.hr/",
  "https://cadalys.breezy.hr/",
  "https://ouai.breezy.hr/",
  "https://breachquest.breezy.hr/",
  "https://volta-trucks.breezy.hr/",
  "https://twelve-consulting-group.breezy.hr/",
  "https://bcc.breezy.hr/",
  "https://scentbird.breezy.hr/",
  "https://inspire-hospice-and-palliative-care.breezy.hr/",
  "https://costanzo-s-bakery.breezy.hr/",
  "https://pet-palace.breezy.hr/",
  "https://chess-wizards.breezy.hr/",
  "https://continued.breezy.hr/",
  "https://dodge.breezy.hr/",
  "https://ouai.breezy.hr/",
  "https://courted.breezy.hr/",
  "https://gold-road.breezy.hr/",
  "https://ezyvet.breezy.hr/",
  "https://pitstop-connect.breezy.hr/",
  "https://twelve-consulting-group.breezy.hr/",
  "https://thirdchannel-inc.breezy.hr/",
  "https://love-corn.breezy.hr/",
  "https://ezoic-inc.breezy.hr/",
  "https://noble-live-in-care.breezy.hr/",
  "https://etain-health.breezy.hr/"
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