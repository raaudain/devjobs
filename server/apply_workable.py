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

words = "./data/params/smartrecruiters.txt"
www = r"https://careers.smartrecruiters.com/(.*?)/"
link = "https://careers.smartrecruiters.com"


f = open(words, "r")
text = [company.lower().strip() for company in f]
f.close()


duck = [
    "https://careers.smartrecruiters.com/OLXBrasil",
    "https://careers.smartrecruiters.com/WAREMARenkhoffSE",
    "https://careers.smartrecruiters.com/Krombacher1",
    "https://careers.smartrecruiters.com/linktag",
    "https://careers.smartrecruiters.com/SnowSoftware",
    "https://careers.smartrecruiters.com/WesternDigital",
    "https://careers.smartrecruiters.com/MinorInternational",
    "https://careers.smartrecruiters.com/Deloitte6",
    "https://careers.smartrecruiters.com/WabashValleyPowerAlliance",
    "https://careers.smartrecruiters.com/KellyServicesEu",
    "https://careers.smartrecruiters.com/KIABI",
    "https://careers.smartrecruiters.com/AssociatedMaterials",
    "https://careers.smartrecruiters.com/WiproDigital",
    "https://careers.smartrecruiters.com/NazarbayevUniversity1",
    "https://careers.smartrecruiters.com/AptiveEnvironmental1",
    "https://careers.smartrecruiters.com/ENLYZE",
    "https://careers.smartrecruiters.com/MFMB",
    "https://careers.smartrecruiters.com/SiaPartners",
    "https://careers.smartrecruiters.com/HagieManufacturingCompany",
    "https://careers.smartrecruiters.com/IDB",
    "https://careers.smartrecruiters.com/JACOBSDOUWEEGBERTS",
    "https://careers.smartrecruiters.com/InterIKEAGroup",
    "https://careers.smartrecruiters.com/CheckpointSystems",
    "https://careers.smartrecruiters.com/Cromology/",
    "https://careers.smartrecruiters.com/Lesaffre",
    "https://careers.smartrecruiters.com/NAPAAUTOPARTS",
    "https://careers.smartrecruiters.com/WestgateResorts",
    "https://careers.smartrecruiters.com/OCP",
    "https://careers.smartrecruiters.com/ChristianBrothersAutomotive",
    "https://careers.smartrecruiters.com/Hospicegeneral",
    "https://careers.smartrecruiters.com/TheracareINC",
    "https://careers.smartrecruiters.com/SanaCommerce",
    "https://careers.smartrecruiters.com/Equinox",
    "https://careers.smartrecruiters.com/huntRED",
    "https://careers.smartrecruiters.com/BlueScopeBuildingsNorthAmerica",
    "https://careers.smartrecruiters.com/AnalygenceInc",
    "https://careers.smartrecruiters.com/Flink3",
    "https://careers.smartrecruiters.com/TescoTechnologyCE",
    "https://careers.smartrecruiters.com/DeltaElectronics",
    "https://careers.smartrecruiters.com/Square",
    "https://careers.smartrecruiters.com/ABOUTYOUGmbH",
    "https://careers.smartrecruiters.com/NorcoInc1",
    "https://careers.smartrecruiters.com/INNOVIEW",
    "https://careers.smartrecruiters.com/HuaweiTechnologiesCanadaCoLtd",
    "https://careers.smartrecruiters.com/Edenred",
    "https://careers.smartrecruiters.com/Devexperts",
    "https://careers.smartrecruiters.com/CorrectCraft",
    "https://careers.smartrecruiters.com/FannieMae",
    "https://careers.smartrecruiters.com/IODigital",
    "https://careers.smartrecruiters.com/Resultant",
    "https://careers.smartrecruiters.com/Leetchi",
    "https://careers.smartrecruiters.com/publicisgroupe",
    "https://careers.smartrecruiters.com/InformaGroupPlc",
    "https://careers.smartrecruiters.com/Socotec",
    "https://careers.smartrecruiters.com/Comoto",
    "https://careers.smartrecruiters.com/MarshallADG",
    "https://careers.smartrecruiters.com/Renaissance",
    "https://careers.smartrecruiters.com/IKEABulgaria",
    "https://careers.smartrecruiters.com/genomicsengland",
    "https://careers.smartrecruiters.com/RocketInternet",
    "https://careers.smartrecruiters.com/Leetchi",
    "https://careers.smartrecruiters.com/publicisgroupe",
    "https://careers.smartrecruiters.com/InformaGroupPlc",
    "https://careers.smartrecruiters.com/Socotec",
    "https://careers.smartrecruiters.com/Comoto",
    "https://careers.smartrecruiters.com/MarshallADG",
    "https://careers.smartrecruiters.com/Renaissance",
    "https://careers.smartrecruiters.com/IKEABulgaria",
    "https://careers.smartrecruiters.com/genomicsengland",
    "https://careers.smartrecruiters.com/RocketInternet",
    "https://careers.smartrecruiters.com/LVMHPerfumesCosmetics",
    "https://careers.smartrecruiters.com/MVIGroupGmbH",
    "https://careers.smartrecruiters.com/MRValuationConsultingLLC",
    "https://careers.smartrecruiters.com/UNLEASH",
    "https://careers.smartrecruiters.com/CapTechConsulting",
    "https://careers.smartrecruiters.com/CocuSocial",
    "https://careers.smartrecruiters.com/RodeoFX",
    "https://careers.smartrecruiters.com/CustomizedEnergySolutions",
    "https://careers.smartrecruiters.com/ImplementConsultingGroup",
    "https://careers.smartrecruiters.com/SaludFamilyHealthCenters",
    "https://careers.smartrecruiters.com/LVMHPerfumesCosmetics",
    "https://careers.smartrecruiters.com/MVIGroupGmbH",
    "https://careers.smartrecruiters.com/MRValuationConsultingLLC",
    "https://careers.smartrecruiters.com/UNLEASH",
    "https://careers.smartrecruiters.com/CapTechConsulting",
    "https://careers.smartrecruiters.com/CocuSocial",
    "https://careers.smartrecruiters.com/RodeoFX",
    "https://careers.smartrecruiters.com/CustomizedEnergySolutions",
    "https://careers.smartrecruiters.com/ImplementConsultingGroup",
    "https://careers.smartrecruiters.com/SaludFamilyHealthCenters",
    "https://careers.smartrecruiters.com/AUTODOC",
    "https://careers.smartrecruiters.com/OliverBonacini",
    "https://careers.smartrecruiters.com/ikeamexico",
    "https://careers.smartrecruiters.com/HUG",
    "https://careers.smartrecruiters.com/87seconds",
    "https://careers.smartrecruiters.com/CASES",
    "https://careers.smartrecruiters.com/EyasGaming",
    "https://careers.smartrecruiters.com/VillageGreen1",
    "https://careers.smartrecruiters.com/IKEASouthEastAsia",
    "https://careers.smartrecruiters.com/artoftransfer",
    "https://careers.smartrecruiters.com/CommunityHealthcareNetwork",
    "https://careers.smartrecruiters.com/UniversityOfRochesterMedicalCenter",
    "https://careers.smartrecruiters.com/SHAPETechnologiesGroup",
    "https://careers.smartrecruiters.com/AdeebaEServicesPvtLtd",
    "https://careers.smartrecruiters.com/MarinerPartnersInc",
    "https://careers.smartrecruiters.com/HarscoCorporation1",
    "https://careers.smartrecruiters.com/DaisyGroup1",
    "https://careers.smartrecruiters.com/SeniorCommUnityCareOfNorthCarolina",
    "https://careers.smartrecruiters.com/PacificLinksInternationalLLC",
    "https://careers.smartrecruiters.com/brainrider",
    "https://careers.smartrecruiters.com/LextorahLDS",
    "https://careers.smartrecruiters.com/BestWesternHotelsResorts",
    "https://careers.smartrecruiters.com/EASYRECRUE",
    "https://careers.smartrecruiters.com/PublicOutreach",
    "https://careers.smartrecruiters.com/Ekipa",
    "https://careers.smartrecruiters.com/GBM1",
    "https://careers.smartrecruiters.com/prosidianconsulting",
    "https://careers.smartrecruiters.com/JobStoreStaffing",
    "https://careers.smartrecruiters.com/tsagroup",
    "https://careers.smartrecruiters.com/ContactEnergy",
    "https://careers.smartrecruiters.com/Brainlab",
    "https://careers.smartrecruiters.com/EnprotechCorp",
    "https://careers.smartrecruiters.com/AssureDentalFamilyCareBraces",
    "https://careers.smartrecruiters.com/Powerhouse1",
    "https://careers.smartrecruiters.com/AGTechnologies1",
    "https://careers.smartrecruiters.com/Kioxia",
    "https://careers.smartrecruiters.com/Cermaticom",
    "https://careers.smartrecruiters.com/Exelixis1",
    "https://careers.smartrecruiters.com/EJOBS",
    "https://careers.smartrecruiters.com/AskITConsulting",
    "https://careers.smartrecruiters.com/HuaweiTechnologiesUSA",
    "https://careers.smartrecruiters.com/BlueOptima",
    "https://careers.smartrecruiters.com/Bringme2",
    "https://careers.smartrecruiters.com/AdeebaEServicesPvtLtd2",
    "https://careers.smartrecruiters.com/trinitashcs",
    "https://careers.smartrecruiters.com/VAMS",
    "https://careers.smartrecruiters.com/InspiraMarketing",
    "https://careers.smartrecruiters.com/granbyranch",
    "https://careers.smartrecruiters.com/LinkedIn3",
    "https://careers.smartrecruiters.com/GoodwillIndustriesOfKanawhaValle",
    "https://careers.smartrecruiters.com/TotalSpecificSolutions",
    "https://careers.smartrecruiters.com/Triipme",
    "https://careers.smartrecruiters.com/TonicDNA1",
    "https://careers.smartrecruiters.com/TheMorningStarCompany",
    "https://careers.smartrecruiters.com/DigitalWholesaleSolutions",
    "https://careers.smartrecruiters.com/rue21",
    "https://careers.smartrecruiters.com/Mindship",
    "https://careers.smartrecruiters.com/SouthernMedicalRecruiters",
    "https://careers.smartrecruiters.com/EACOMTimberCorporation",
    "https://careers.smartrecruiters.com/Lostar",
    "https://careers.smartrecruiters.com/crownci",
    "https://careers.smartrecruiters.com/SPTHoldings",
    "https://careers.smartrecruiters.com/CaliforniaISO",
    "https://careers.smartrecruiters.com/USPAInternational",
    "https://careers.smartrecruiters.com/BizMutMarketingGmbH",
    "https://careers.smartrecruiters.com/IBIGroup",
    "https://careers.smartrecruiters.com/Hoistgroup",
    "https://careers.smartrecruiters.com/AUTENTISpZOo",
    "https://careers.smartrecruiters.com/ShermanPoleBuildings",
    "https://careers.smartrecruiters.com/STCU1",
    "https://careers.smartrecruiters.com/EthosInteractive",
    "https://careers.smartrecruiters.com/pirsonal",
    "https://careers.smartrecruiters.com/DynamicSoftware1",
    "https://careers.smartrecruiters.com/IFS1",
    "https://careers.smartrecruiters.com/MissionCityCommunityNetwork",
    "https://careers.smartrecruiters.com/LkaPeopleLtd",
    "https://careers.smartrecruiters.com/AarnaHRSolutionsPvtLtd",
    "https://careers.smartrecruiters.com/NYMarketingFirm",
    "https://careers.smartrecruiters.com/WinMaxSystemsCorporation",
    "https://careers.smartrecruiters.com/MulticulturalLearningCenterCharterSchool",
    "https://careers.smartrecruiters.com/Iqarus",
    "https://careers.smartrecruiters.com/OUICAREGROUP",
    "https://careers.smartrecruiters.com/Chainio",
    "https://careers.smartrecruiters.com/DarumaCorporation",
    "https://careers.smartrecruiters.com/ContechsConsultingLimited",
    "https://careers.smartrecruiters.com/HiTechSolutions",
    "https://careers.smartrecruiters.com/NewYorkPsychotherapyAndCounselingCenter",
    "https://careers.smartrecruiters.com/PrimeLineUtilityServices",
    "https://careers.smartrecruiters.com/NorthgatePublicServices",
    "https://careers.smartrecruiters.com/UhligLLC",
    "https://careers.smartrecruiters.com/AbercrombieAndFitchCo",
    "https://careers.smartrecruiters.com/SycomoreAssetManagement",
    "https://careers.smartrecruiters.com/Sosemo",
    "https://careers.smartrecruiters.com/Acomodeo",
    "https://careers.smartrecruiters.com/Conga1",
    "https://careers.smartrecruiters.com/INTTechnologies",
    "https://careers.smartrecruiters.com/behaviorchangeinstitutellc",
    "https://careers.smartrecruiters.com/Salespeople",
    "https://careers.smartrecruiters.com/AbstractRecruitment",
    "https://careers.smartrecruiters.com/bigshift",
    "https://careers.smartrecruiters.com/Crossmedia",
    "https://careers.smartrecruiters.com/WJCompany",
    "https://careers.smartrecruiters.com/USITSolutionsInc",
    "https://careers.smartrecruiters.com/Varrlyn",
    "https://careers.smartrecruiters.com/DECATHLON",
    "https://careers.smartrecruiters.com/RocknRoll1",
    "https://careers.smartrecruiters.com/ClearPointRecruitment",
    "https://careers.smartrecruiters.com/TurnerTownsend",
    "https://careers.smartrecruiters.com/IVADOLabs",
    "https://careers.smartrecruiters.com/Avostart",
    "https://careers.smartrecruiters.com/SalvusHealth",
    "https://careers.smartrecruiters.com/PharosAcademyCharterSchool",
    "https://careers.smartrecruiters.com/STJOSEPHCENTER",
    "https://careers.smartrecruiters.com/Rituals1",
    "https://careers.smartrecruiters.com/NuViewConnectionsInc",
    "https://careers.smartrecruiters.com/PixelleSpecialtySolutions",
    "https://careers.smartrecruiters.com/Structube1",
    "https://careers.smartrecruiters.com/Heycater",
    "https://careers.smartrecruiters.com/PremiumTechnology",
    "https://careers.smartrecruiters.com/AngionBiomedica",
    "https://careers.smartrecruiters.com/CCIConsulting",
    "https://careers.smartrecruiters.com/SanmaxInc",
    "https://careers.smartrecruiters.com/EOCTEBP",
    "https://careers.smartrecruiters.com/PerfectDynamicsVirtualSolutionsLLC",
    "https://careers.smartrecruiters.com/RenardResources",
    "https://careers.smartrecruiters.com/EleveursDesSavoie1",
    "https://careers.smartrecruiters.com/Liongard",
    "https://careers.smartrecruiters.com/ChateaudePommard",
    "https://careers.smartrecruiters.com/HarveyBericAssociatesLtd",
    "https://careers.smartrecruiters.com/ManitoulinGroupOfCompanies",
    "https://careers.smartrecruiters.com/TexasHealthResources",
    "https://careers.smartrecruiters.com/TechnamoLLC",
    "https://careers.smartrecruiters.com/InvinityEnergySystems",
    "https://careers.smartrecruiters.com/Viaco1",
    "https://careers.smartrecruiters.com/seakrengineering",
    "https://careers.smartrecruiters.com/TeamViewer1",
    "https://careers.smartrecruiters.com/KennedyEmploymentSolutions",
    "https://careers.smartrecruiters.com/StryberAG",
    "https://careers.smartrecruiters.com/BMSInternational",
    "https://careers.smartrecruiters.com/Insightsoftware",
    "https://careers.smartrecruiters.com/SonsoftInc",
    "https://careers.smartrecruiters.com/SoftwarePeopleInc",
    "https://careers.smartrecruiters.com/MarketAxess",
    "https://careers.smartrecruiters.com/Lithium3TechnologyRecruitmentLimited",
    "https://careers.smartrecruiters.com/HighCater",
    "https://careers.smartrecruiters.com/TescoBengaluru",
    "https://careers.smartrecruiters.com/WakeForestBaptistHealth",
    "https://careers.smartrecruiters.com/RheindataGmbH",
    "https://careers.smartrecruiters.com/KonnectRecruitmentLimited",
    "https://careers.smartrecruiters.com/BlueprintManagementGroup",
    "https://careers.smartrecruiters.com/AimcoApartmentHomes",
    "https://careers.smartrecruiters.com/WhyHotel",
    "https://careers.smartrecruiters.com/goldstonepartners",
    "https://careers.smartrecruiters.com/EnerkemInc",
    "https://careers.smartrecruiters.com/PhishedBV",
    "https://careers.smartrecruiters.com/SGS",
    "https://careers.smartrecruiters.com/BelovedCommunityCharterSchool",
    "https://careers.smartrecruiters.com/GlobalChannelManagementInc",
    "https://careers.smartrecruiters.com/ChartpakInc",
    "https://careers.smartrecruiters.com/epochgames",
    "https://careers.smartrecruiters.com/ClientSolvTechnologies",
    "https://careers.smartrecruiters.com/SaxonGlobal",
    "https://careers.smartrecruiters.com/SituationsVacantLtd",
    "https://careers.smartrecruiters.com/PerScholas",
    "https://careers.smartrecruiters.com/MercyHousing",
    "https://careers.smartrecruiters.com/SedusGruppe",
    "https://careers.smartrecruiters.com/UrbanConsulting",
    "https://careers.smartrecruiters.com/KalaPharmaceuticalsInc",
    "https://careers.smartrecruiters.com/HomeHealthDepot1",
    "https://careers.smartrecruiters.com/SynchronyGroup",
    "https://careers.smartrecruiters.com/AngloAmericanDeBeersGroup",
    "https://careers.smartrecruiters.com/EdifySoftwareConsulting",
    "https://careers.smartrecruiters.com/FranxBV",
    "https://careers.smartrecruiters.com/MetasysTechnologiesInc1",
    "https://careers.smartrecruiters.com/CellularDynamics",
    "https://careers.smartrecruiters.com/SiteMasterInc",
    "https://careers.smartrecruiters.com/eqeep",
    "https://careers.smartrecruiters.com/tocgrp",
    "https://careers.smartrecruiters.com/Ateeca",
    "https://careers.smartrecruiters.com/ZentechConsulting",
    "https://careers.smartrecruiters.com/EPROINC",
    "https://careers.smartrecruiters.com/studentsocietymcgilluniversity",
    "https://careers.smartrecruiters.com/DonardRecruitment",
    "https://careers.smartrecruiters.com/MedlineAustralia",
    "https://careers.smartrecruiters.com/TorchysTacos",
    "https://careers.smartrecruiters.com/ValidationEngineeringGroup",
    "https://careers.smartrecruiters.com/Nexthink",
    "https://careers.smartrecruiters.com/THERESOLUTEGROUPLIMITED",
    "https://careers.smartrecruiters.com/CatholicHealthcareLimited2",
    "https://careers.smartrecruiters.com/Devex1",
    "https://careers.smartrecruiters.com/HighFiveDental",
    "https://careers.smartrecruiters.com/SuttonTransport",
    "https://careers.smartrecruiters.com/ITEXCELLLC",
    "https://careers.smartrecruiters.com/Eatwith",
    "https://careers.smartrecruiters.com/EdosoftFactory",
    "https://careers.smartrecruiters.com/ODIONGmbH",
    "https://careers.smartrecruiters.com/VistaPrairieCommunities",
    "https://careers.smartrecruiters.com/KelltonTech",
    "https://careers.smartrecruiters.com/TELEIOSRecruitmentLtd",
    "https://careers.smartrecruiters.com/SmileDentalGroup",
    "https://careers.smartrecruiters.com/SumeruSolutions1",
    "https://careers.smartrecruiters.com/Jeeon",
    "https://careers.smartrecruiters.com/ColumbiaUniversity1",
    "https://careers.smartrecruiters.com/BeyondConsultingSolutions",
    "https://careers.smartrecruiters.com/SynergyRecruitment1",
    "https://careers.smartrecruiters.com/AWSTruepower",
    "https://careers.smartrecruiters.com/LeoPharma",
    "https://careers.smartrecruiters.com/KaizenTalentSolutionsLimited",
    "https://careers.smartrecruiters.com/EagleRecruit",
    "https://careers.smartrecruiters.com/Wizikey",
    "https://careers.smartrecruiters.com/RICEFWTechnologiesInc1",
    "https://careers.smartrecruiters.com/JYSK",
    "https://careers.smartrecruiters.com/CapitalDigestiveCare",
    "https://careers.smartrecruiters.com/VMDCorp",
    "https://careers.smartrecruiters.com/Labforward",
    "https://careers.smartrecruiters.com/CopiousSoftware",
    "https://careers.smartrecruiters.com/RIDICorp",
    "https://careers.smartrecruiters.com/MiseEnPlaceLondon",
    "https://careers.smartrecruiters.com/dalesmithey",
    "https://careers.smartrecruiters.com/Wellcare3",
    "https://careers.smartrecruiters.com/TivertonAdvisors",
    "https://careers.smartrecruiters.com/MicrosoftC1",
    "https://careers.smartrecruiters.com/CoxEnterprises2",
    "https://careers.smartrecruiters.com/HarbisonWalkerInternational",
    "https://careers.smartrecruiters.com/SSENSE1",
    "https://careers.smartrecruiters.com/CityofPhiladelphia",
    "https://careers.smartrecruiters.com/THECLIMATECHOICEUGhaftungsbeschrnkt",
    "https://careers.smartrecruiters.com/SussexRecruitmentLtd",
    "https://careers.smartrecruiters.com/IUNGOSpA",
    "https://careers.smartrecruiters.com/ThePlace1",
]

w = []
added = set()
for i in duck:
    # print(i)
    word = re.findall(www, i)
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