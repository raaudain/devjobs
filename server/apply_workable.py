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

words = "./data/params/ashbyhq.txt"
www = r"https://jobs.ashbyhq.com/(.*?)/"
link = "https://jobs.ashbyhq.com"


f = open(words, "r")
text = [company.lower().strip() for company in f]
f.close()


duck = [
  "https://jobs.ashbyhq.com/ready",
  "https://jobs.ashbyhq.com/leadiq/",
  "https://jobs.ashbyhq.com/treasuryprime/3f8b015a-e161-4947-9c03-9f5119d9550b",
  "https://jobs.ashbyhq.com/standard/2bc8e78d-5e92-4742-911d-b7b9048f94d0",
  "https://jobs.ashbyhq.com/standard/3fd28445-62e5-4b38-88ad-ec8244358d1f",
  "https://jobs.ashbyhq.com/memora/544dec5a-087a-4d97-a8b9-cd2330c98fa1",
  "https://jobs.ashbyhq.com/commsor/8a0a1235-0603-4cf5-9b58-0e64ccf71302",
  "https://jobs.ashbyhq.com/commsor/23d628be-93b6-4a8b-bd56-4543aad93b6e",
  "https://jobs.ashbyhq.com/standard/747cf8e5-1e5f-41b2-895a-de37811576cf",
  "https://jobs.ashbyhq.com/firstbase/7453df44-f1f9-4022-b298-7eafc8318589?embed=true",
  "https://jobs.ashbyhq.com/standard/1d606f27-655a-4105-9f2d-8711cdfa2acd",
  "https://jobs.ashbyhq.com/standard/defd153b-4dc9-4c37-b3ef-5ed36fd836df",
  "https://jobs.ashbyhq.com/memora/578af80b-85d7-4eaa-ab75-a6b26e3f9c8e",
  "https://jobs.ashbyhq.com/commsor/d92e41dd-0f36-4418-a2d2-f48516841cb8",
  "https://jobs.ashbyhq.com/juked/ab3b4d29-cda0-4593-839a-874b2397d9e8",
  "https://jobs.ashbyhq.com/standard/b1f12f6e-88aa-49fb-8a4d-2dfed4be19b0",
  "https://jobs.ashbyhq.com/belvo/e1a326cb-a89b-4128-8fa4-5814bf377efe/application",
  "https://jobs.ashbyhq.com/treasuryprime/6831bfe2-9a0a-4bda-835c-f58484a4e16c",
  "https://jobs.ashbyhq.com/Convictional/8ea5bc1a-41da-491a-8f38-c22648a3d43e",
  "https://jobs.ashbyhq.com/modernfertility/f5e16438-8c4d-47af-a2e7-38c86565717e",
  "https://jobs.ashbyhq.com/Deel/8f89ebc8-d77f-4daa-9b38-88a5ae586f63",
  "https://jobs.ashbyhq.com/belvo/07d62dba-6d9e-4a2c-9652-36a07431874e",
  "https://jobs.ashbyhq.com/ycombinator/242ef73e-c89e-4a50-9cd4-e91f275805f8",
  "https://jobs.ashbyhq.com/belvo/402d1fa0-33d9-4884-8540-2fb27acf930a",
  "https://jobs.ashbyhq.com/Alpaca/41616dcc-a2d3-47ac-a250-c266148d4318",
  "https://jobs.ashbyhq.com/treasuryprime/4d83049d-6388-46e5-bb6d-0f118ceb2c6d",
  "https://jobs.ashbyhq.com/modernfertility/ec972c70-7c20-4608-9a84-ecdcc129b17d",
  "https://jobs.ashbyhq.com/firstbase/4ef59ab2-acab-4fa2-bcc2-69429d9ac233?embed=true",
  "https://jobs.ashbyhq.com/Ashby/f99c1c4a-07f5-42fa-987e-de9a93f945dd",
  "https://jobs.ashbyhq.com/treasuryprime/ed3d704c-c970-411c-9e03-e61758ae14cb",
  "https://jobs.ashbyhq.com/topia",
  "https://jobs.ashbyhq.com/upflow",
  "https://jobs.ashbyhq.com/OctoML",
  "https://jobs.ashbyhq.com/bigeye",
  "https://jobs.ashbyhq.com/standard/e46af3ce-c96a-4005-8abd-59d1f3fcc914",
  "https://jobs.ashbyhq.com/standard/a11007b5-3b40-4944-b73e-1ce959246fc8",
  "https://jobs.ashbyhq.com/transform/1a4fb047-5b60-4e93-872a-73e472c4b20d",
  "https://jobs.ashbyhq.com/moderntreasury/dc9bcfe8-64ef-4377-ad74-0cdbca3be694",
  "https://jobs.ashbyhq.com/Pipeline/",
  "https://jobs.ashbyhq.com/firstbase/7453df44-f1f9-4022-b298-7eafc8318589?embed=true",
  "https://jobs.ashbyhq.com/Deel/a6fcef08-90a7-482e-84b2-e8f46a8a16b3",
  "https://jobs.ashbyhq.com/upflow/e5b0ff25-f60c-4761-8042-9040797154a7/application",
  "https://jobs.ashbyhq.com/firstbase/4ef59ab2-acab-4fa2-bcc2-69429d9ac233?embed=true",
  "https://jobs.ashbyhq.com/Ashby/f99c1c4a-07f5-42fa-987e-de9a93f945dd",
  "https://jobs.ashbyhq.com/upflow/4c4c8538-8d93-4856-ae0b-669316ad6898/application",
  "https://jobs.ashbyhq.com/standard/e32fdf8d-61ef-40e4-9b5f-1f0431893246",
  "https://jobs.ashbyhq.com/modernfertility/36815c80-fc6c-4912-929b-97be51187db6",
  "https://jobs.ashbyhq.com/treasuryprime/9b9fee1e-7eca-4208-b4ef-e991fee9205d",
  "https://jobs.ashbyhq.com/Alpaca/41616dcc-a2d3-47ac-a250-c266148d4318",
  "https://jobs.ashbyhq.com/transform/30ef369c-5cf9-4619-9ce7-6a115ba79ba3",
  "https://jobs.ashbyhq.com/Ashby/3aee80da-4b17-46eb-bfc5-85b59ef850da",
  "https://jobs.ashbyhq.com/standard/a97462b2-9e01-4ea3-89e5-6ee22201ed0d",
  "https://jobs.ashbyhq.com/Deel/28154475-e3a1-4cbd-bd33-e452ac495bb3?ref=nodesk",
  "https://jobs.ashbyhq.com/commsor/d7feccab-0eb3-4910-81fd-6d8c359d1f8e",
  "https://jobs.ashbyhq.com/census/15d26836-4603-4b1f-87d5-8c9f101311e3",
  "https://jobs.ashbyhq.com/transform/b1d201ec-8009-4a53-9e9c-927389934d08",
  "https://jobs.ashbyhq.com/Deel/95a01831-3894-43af-87a8-660963f59c9f",
  "https://jobs.ashbyhq.com/duneanalytics/c8eb493c-e952-472e-a7c2-dc3d0e277421",
  "https://jobs.ashbyhq.com/belvo/08425968-5a4b-49d2-bc7d-fac950e9ca1c",
  "https://jobs.ashbyhq.com/leadiq/5e0bb699-69d5-444c-a678-0b9419b1ede2",
  "https://jobs.ashbyhq.com/belvo/4bb0b898-a6e2-4362-bd3c-3c6f481fdf4e",
  "https://jobs.ashbyhq.com/duneanalytics/b5f58cf2-d021-4df0-b500-ebc215f7f4f6",
  "https://jobs.ashbyhq.com/belvo/a51bf754-fc4e-4576-99a6-adb112a73859",
  "https://jobs.ashbyhq.com/treasuryprime/68c1532e-2015-4d21-a058-f43f9e9c078b",
  "https://jobs.ashbyhq.com/standard/1027ef53-30a9-4379-a142-f03691bb33c6",
  "https://jobs.ashbyhq.com/treasuryprime/95abd3ee-776e-47a5-8640-b3d14cdb37e7",
  "https://jobs.ashbyhq.com/Deel/8bfbb15a-da48-40a8-92bf-68b8efa86328",
  "https://jobs.ashbyhq.com/ycombinator/c093ffa1-e638-4fd9-86bc-97663ab6d0b8",
  "https://jobs.ashbyhq.com/belvo/845611d1-8a4a-4753-91de-7945847bcb4c",
  "https://jobs.ashbyhq.com/ycombinator/8aa099e3-8dab-41db-946e-69a3a4209c11",
  "https://jobs.ashbyhq.com/Deel/ae2ae4fc-dbe9-4285-8156-b021e1e666f0",
  "https://jobs.ashbyhq.com/belvo/5f235ec9-6e1d-4ce2-a775-4824a66b63a7",
  "https://jobs.ashbyhq.com/duneanalytics/9b60ec09-06a7-43ec-b162-339734f4d168",
  "https://jobs.ashbyhq.com/memora/aeffbcea-c088-409e-8513-6b1a1fa35456",
  "https://jobs.ashbyhq.com/belvo/cb925a09-a85e-4f83-9ff0-f94071b104d6",
  "https://jobs.ashbyhq.com/belvo/e1a326cb-a89b-4128-8fa4-5814bf377efe",
  "https://jobs.ashbyhq.com/Deel/da7069c9-64fc-46fe-a22b-6f5d742c9b68",
  "https://jobs.ashbyhq.com/belvo/b8bf3377-62bc-4596-a46e-e95b8813bdf1",
  "https://jobs.ashbyhq.com/belvo/9ad0d4d9-8831-4f5a-8089-ac559c778793"
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
        a.write(f"{d}\n")
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