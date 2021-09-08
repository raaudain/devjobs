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

# words = "./data/params/breezyhr.txt"
# www = r"https://(.*?).breezy.hr/"
# link = "https://jobs.ashbyhq.com"

# words = "./data/params/jobvite.txt"
# www = r"https://jobs.jobvite.com/careers/(.*?)/"
# # link = "https://jobs.ashbyhq.com"

words = "./data/params/recruiterbox.txt"
www = r"https://(.*?).recruiterbox.com/jobs"
# link = "https://jobs.ashbyhq.com"


f = open(words, "r")
text = [company.lower().strip() for company in f]
f.close()


duck = [
'https://cardinaleducation.recruiterbox.com/jobs',
'https://skit.recruiterbox.com/jobs',
'https://mekari.recruiterbox.com/jobs',
'https://vastbroadband.recruiterbox.com/jobs',
'https://leamseducation.recruiterbox.com/jobs',
'https://espoc.recruiterbox.com/jobs',
'https://watcha.recruiterbox.com/jobs',
'https://discoverwork.recruiterbox.com/jobs',
'https://medibuddy.recruiterbox.com/jobs',
'https://bookmyshow.recruiterbox.com/jobs',
'https://veiovis.recruiterbox.com/jobs',
'https://wodify.recruiterbox.com/jobs',
'https://sharechat.recruiterbox.com/jobs',
'https://givedirectly.recruiterbox.com/jobs',
'https://cambrio.recruiterbox.com/jobs',
'https://worksuites.recruiterbox.com/jobs',
'https://fundthatflip.recruiterbox.com/jobs',
'https://pernixllc.recruiterbox.com/jobs',
'https://runtastic.recruiterbox.com/jobs',
'https://mastree.recruiterbox.com/jobs',
'https://weworkindia.recruiterbox.com/jobs',
'https://proletariat.recruiterbox.com/jobs',
'https://wingaviation24226.recruiterbox.com/jobs',
'https://tunda.recruiterbox.com/jobs',
'https://octoml.recruiterbox.com/jobs',
'https://myaussietutor.recruiterbox.com/jobs',
'https://glenrecruiter.recruiterbox.com/jobs',
'https://accfb.recruiterbox.com/jobs',
'https://medicast.recruiterbox.com/jobs',
'https://wufspa.recruiterbox.com/jobs',
'https://ihjez.recruiterbox.com/jobs',
'https://hostgee.recruiterbox.com/jobs',
'https://camerite.recruiterbox.com/jobs',
'https://bijak.recruiterbox.com/jobs',
'https://thesegovia.recruiterbox.com/jobs',
'https://mind.recruiterbox.com/jobs',
'https://x1group.recruiterbox.com/jobs',
'https://10wickets.recruiterbox.com/jobs',
'https://webfy.recruiterbox.com/jobs',
'https://manav.recruiterbox.com/jobs',
'https://dipti.recruiterbox.com/jobs',
'https://elagaan.recruiterbox.com/jobs',
'https://worldstartvm.recruiterbox.com/jobs',
'https://learndash.recruiterbox.com/jobs',
'https://careeradex.recruiterbox.com/jobs',
'https://alaska.recruiterbox.com/jobs',
'https://designer.recruiterbox.com/jobs',
'https://vasoul.recruiterbox.com/jobs',
'https://justinspire.recruiterbox.com/jobs',
'https://sodexoangola.recruiterbox.com/jobs',
'https://testanis.recruiterbox.com/jobs',
'https://phaicu.recruiterbox.com/jobs',
'https://synage.recruiterbox.com/jobs',
'https://effectly.recruiterbox.com/jobs',
'https://helixstudios.recruiterbox.com/jobs',
'https://selco.recruiterbox.com/jobs',
'https://ecartes.recruiterbox.com/jobs',
'https://vispa.recruiterbox.com/jobs',
'https://gcsn.recruiterbox.com/jobs',
'https://infosys.recruiterbox.com/jobs',
'https://ovballfinanz.recruiterbox.com/jobs',
'https://sunmoonstays.recruiterbox.com/jobs',
'https://armature.recruiterbox.com/jobs',
'https://trob.recruiterbox.com/jobs',
'https://andelcare.recruiterbox.com/jobs',
'https://ceba.recruiterbox.com/jobs',
'https://mainebhr.recruiterbox.com/jobs/fk0qple/',
'https://dito.recruiterbox.com/jobs/fk0jk3d/',
'https://funkycorp.recruiterbox.com/jobs/fk0qm7b/',
'https://lifepathsystems.recruiterbox.com/jobs/fk0uyoa',
'https://janickiindustries.recruiterbox.com/jobs/fk0ut3k/',
'https://prempack.recruiterbox.com/jobs/fk0utsn',
'https://vaughnconstruction.recruiterbox.com/jobs/fk0uy1l/',
'https://stateofnewmexico.recruiterbox.com/jobs/fk0q97m/',
'https://celtra.recruiterbox.com/jobs/fk0usbf/',
'https://advancedspace.recruiterbox.com/jobs/fk0uxu4',
'https://ulinkagritech.recruiterbox.com/jobs/fk0ufh9/',
'https://binghamacademy.recruiterbox.com/jobs/fk03c6f/',
'https://aquabluepools.recruiterbox.com/jobs/fk01bc1/',
'https://infracore.recruiterbox.com/jobs/fk0qunz/',
'https://bayareacs.recruiterbox.com/jobs/fk01o6n/',
'https://marketenginuity.recruiterbox.com/jobs/fk0s17v/',
'https://mainebhr.recruiterbox.com/jobs/fk0smkd/',
'https://mybankwell.recruiterbox.com/jobs/fk0u9jx/',
'https://spire.recruiterbox.com/jobs/fk0q76v/',
'https://richelieu.recruiterbox.com/jobs/fk0unwc/',
'https://givedirectly.recruiterbox.com/jobs/fk0uy4n/',
'https://brudis.recruiterbox.com/jobs/fk0un1t',
'https://cmed.recruiterbox.com/jobs/fk0u9sv/',
'https://veiovis.recruiterbox.com/jobs/fk0u541/',
'https://concoconstruction.recruiterbox.com/jobs/fk0uayw/',
'https://kyosk.recruiterbox.com/jobs/fk0u9l1/',
'https://tempo.recruiterbox.com/jobs/fk0uetu/',
'https://thalle.recruiterbox.com/jobs/fk0u4o4/',
'https://vikingcruises.recruiterbox.com/jobs/fk0ubrt/',
'https://uberall.recruiterbox.com/jobs/fk0u23b',
'https://namati.recruiterbox.com/jobs/fk0uum3/',
'https://powerauctions.recruiterbox.com/jobs/fk0ukyu/',
'https://witekio.recruiterbox.com/jobs/fk0ujfe/',
'https://quickrelease.recruiterbox.com/jobs/fk0s6b6/',
'https://givedirectly.recruiterbox.com/jobs/fk0sfce/',
'https://vempraglobo.recruiterbox.com/jobs/fk0qm4v',
'https://hireview.recruiterbox.com/jobs/fk0s6q3/',
'https://moengage.recruiterbox.com/jobs/fk0qlvt/',
'https://mysafehaven.recruiterbox.com/jobs/fk06p4e',
'https://fullerton.recruiterbox.com/jobs/fk0uz6p/',
'https://givedirectly.recruiterbox.com/jobs/fk0ul1m/',
'https://teamomni.recruiterbox.com/jobs/fk03t74/',
'https://mysafehaven.recruiterbox.com/jobs/fk0h3cg',
'https://ocat.recruiterbox.com/jobs/22217',
'https://novigo.recruiterbox.com/jobs/fk0qa19/',
'https://subhiksha.recruiterbox.com/jobs/fk0v1s/',
'https://mybankwell.recruiterbox.com/jobs/fk0usdo/',
'https://testhuset.recruiterbox.com/jobs/fk0fgfm/',
'https://ardentlearninginc.recruiterbox.com/jobs/fk0uy9g/',
'https://vaultconsulting.recruiterbox.com/jobs/fk0jfp1/',
'https://humach.recruiterbox.com/jobs/fk0q9r6',
'https://vantagedatacenters.recruiterbox.com/jobs/fk0uxul',
'https://cambridgecomputer.recruiterbox.com/jobs/fk0uxij',
'https://signeasy.recruiterbox.com/jobs/fk0u3eg/',
'https://fundthatflip.recruiterbox.com/jobs/fk0uy32/',
'https://thequantiumgroup.recruiterbox.com/jobs/fk0u2x2/',
'https://synergenhealth.recruiterbox.com/jobs/fk0hkzk',
'https://vaultconsulting.recruiterbox.com/jobs/fk0ub2i/',
'https://mercycorpsniger.recruiterbox.com/jobs/fk0ukq5/',
'https://stillaguamish.recruiterbox.com/jobs/fk0upc1/',
'https://splashlearn.recruiterbox.com/jobs/fk0u2dn/',
'https://concoconstruction.recruiterbox.com/jobs/fk0jgez/',
'https://novigo.recruiterbox.com/jobs/fk0uvic/',
'https://smartwires.recruiterbox.com/jobs/fk0u5b3/',
'https://myagro.recruiterbox.com/jobs/fk0u4ax/',
'https://mainebhr.recruiterbox.com/jobs/fk0sfeq/',
'https://givedirectly.recruiterbox.com/jobs/fk0shyq/',
'https://culinarydropout.recruiterbox.com/jobs/fk0ent/',
'https://odessainc.recruiterbox.com/jobs/fk0qdys/',
'https://northitalia.recruiterbox.com/jobs/fk035y5/',
'https://uberall.recruiterbox.com/jobs/fk0udkn/',
'https://infolytx.recruiterbox.com/jobs/fk0shz6/',
'https://mybankwell.recruiterbox.com/jobs/fk0u8ul',
'https://flowerchild.recruiterbox.com/jobs/fk06nem/',
'https://funkycorp.recruiterbox.com/jobs/fk03g6b/',
'https://murrayhospital.recruiterbox.com/jobs/fk0ucz3/',
'https://scopicsoftware.recruiterbox.com/jobs/fk0sh7e/',
'https://linkbiz.recruiterbox.com/jobs/fk0uucy/',
'https://nycdatascience.recruiterbox.com/jobs/fk03mmo/',
'https://prempack.recruiterbox.com/jobs/fk03jp3/',
'https://lakepointe.recruiterbox.com/jobs/fk0uy9r/',
'https://janickiindustries.recruiterbox.com/jobs/fk0untu/',
'https://uberall.recruiterbox.com/jobs/fk0ujkt/',
'https://eurasiagroup.recruiterbox.com/jobs/fk0sw2p/',
'https://quanergy.recruiterbox.com/jobs/fk0uou2/',
'https://givedirectly.recruiterbox.com/jobs/fk0s1ec/',
'https://acquisconsulting.recruiterbox.com/jobs/fk0uohx/',
'https://lifepathsystems.recruiterbox.com/jobs/fk0u4tg/',
'https://reside.recruiterbox.com/jobs/fk0swyv/',
'https://aciedge79515.recruiterbox.com/jobs/fk03ml6/',
'https://iristelehealth.recruiterbox.com/jobs/fk0u6bs/',
'https://lakepointe.recruiterbox.com/jobs/fk0uuan/',
'https://reside.recruiterbox.com/jobs/fk0uany/',
'https://verisys.recruiterbox.com/jobs/fk0u5eq/',
'https://greenlightplanet.recruiterbox.com/jobs/fk0uewn/',
'https://celtra.recruiterbox.com/jobs/fk0u2dd/',
'https://mainebhr.recruiterbox.com/jobs/fk0qjpb/',
'https://findingclarity.recruiterbox.com/jobs/fk0u512/',
'https://whatfix101.recruiterbox.com/jobs/fk0qpma/',
'https://humancaresystems.recruiterbox.com/jobs/fk0uabz/',
'https://calibrecpa.recruiterbox.com/jobs/fk0u33p/',
'https://richelieu.recruiterbox.com/jobs/fk0uq4n',
'https://seeq.recruiterbox.com/jobs/fk0u5vg/',
'https://binghamacademy.recruiterbox.com/jobs/fk03chk/',
'https://reside.recruiterbox.com/jobs/fk0u5i2/',
'https://culinarydropout.recruiterbox.com/jobs/fk042e/',
'https://lambda3.recruiterbox.com/jobs/fk01tas/',
'https://ugrowthfund.recruiterbox.com/jobs/fk015sx/',
'https://colcare.recruiterbox.com/jobs/fk0uxzc',
'https://athreon.recruiterbox.com/jobs/fk032fy/',
'https://vantagedatacenters.recruiterbox.com/jobs/fk0ufyl/',
'https://vagasdb1.recruiterbox.com/jobs/fk03z23/',
'https://splashlearn.recruiterbox.com/jobs/fk0ugj9/',
'https://northitalia.recruiterbox.com/jobs/fk0mi59/',
'https://seacoast.recruiterbox.com/jobs/fk0uknp/',
'https://kyosk.recruiterbox.com/jobs/fk0u7f5/',
'https://petroliana.recruiterbox.com/jobs/fk0ubar',
'https://locatee.recruiterbox.com/jobs/fk0ukbx/',
'https://fullerton.recruiterbox.com/jobs/05a1bc3725a943678254bfe3806f47dd',
'https://sajenaturalwellnessretail.recruiterbox.com/jobs/fk0358m/',
'https://mainebhr.recruiterbox.com/jobs/fk0shak/',
'https://colcare.recruiterbox.com/jobs/fk0u9mz',
'https://mekari.recruiterbox.com/jobs/fk01bnt/',
'https://latelieranimation.recruiterbox.com/jobs/fk0f9ls/',
'https://mkdelectric79060.recruiterbox.com/jobs/fk0u776/',
'https://vagasdb1.recruiterbox.com/jobs/fk0sw6e/',
'https://altairsw.recruiterbox.com/jobs/fk0uxqz',
'https://parkwestgallery.recruiterbox.com/jobs/fk0jc36/',
'https://richelieu.recruiterbox.com/jobs/fk0u5ea/',
'https://mekari.recruiterbox.com/jobs/fk0f2j3',
'https://culinarydropout.recruiterbox.com/jobs/fk0enq/',
'https://vagasdb1.recruiterbox.com/jobs/72cd866ec9104e66ae7b96b18c992a2c',
'https://flyersenergy.recruiterbox.com/jobs/fk0ubkg/',
'https://develer.recruiterbox.com/jobs/fk0uljm/',
'https://okhi.recruiterbox.com/jobs/fk0us8s/',
'https://fullerton.recruiterbox.com/jobs/4ac2617cda9a4aaaab8e64a24509dd53',
'https://avaaz.recruiterbox.com/jobs/fk0shr3/',
'https://mysafehaven.recruiterbox.com/jobs/fk0qy1i',
'https://linkbiz.recruiterbox.com/jobs/fk06p25/',
'https://wolframresearch.recruiterbox.com/jobs/fk0u4q9/',
'https://signspecialists.recruiterbox.com/jobs/fk0hsmm',
'https://fuel3d.recruiterbox.com/jobs/fk0uyy5/',
'https://vikingcruises.recruiterbox.com/jobs/fk0sfjg/',
'https://wuyee.recruiterbox.com/jobs/fk0uga1/',
'https://colorofchange.recruiterbox.com/jobs/fk0ub1i/',
'https://rocketsofawesome.recruiterbox.com/jobs/fk0sfpg/',
'https://centraldrugsrx.recruiterbox.com/jobs/fk03wya',
'https://shecan.recruiterbox.com/jobs/fk0uezv',
'https://greytip.recruiterbox.com/jobs/fk0ui3h/',
'https://culinarydropout.recruiterbox.com/jobs/fk0en1/',
'https://limejump.recruiterbox.com/jobs/fk0s6q1/',
'https://mercycorpsniger.recruiterbox.com/jobs/fk0sf8d/',
'https://newvoices.recruiterbox.com/jobs/fk0qg3f/',
'https://subhiksha.recruiterbox.com/jobs/fk0jvcm/',
'https://boardofchildcare.recruiterbox.com/jobs/fk0qq44',
'https://develer.recruiterbox.com/jobs/fk01v6j/',
'https://avaaz.recruiterbox.com/jobs/fk0u5n1/',
'https://givedirectly.recruiterbox.com/jobs/fk0sm81/',
'https://terrapower.recruiterbox.com/jobs/fk0udnc',
'https://celtra.recruiterbox.com/jobs/fk0qlp3/',
'https://fiducial.recruiterbox.com/jobs/fk0swu7/',
'https://vempraglobo.recruiterbox.com/jobs/fk0smms/',
'https://thenovakconsultinggroup.recruiterbox.com/jobs/fk0u522/',
'https://mainebhr.recruiterbox.com/jobs/fk0sfl2/',
'https://mainebhr.recruiterbox.com/jobs/fk0ube5/',
'https://aquilacommercial.recruiterbox.com/jobs/fk0s6nj',
'https://culinarydropout.recruiterbox.com/jobs/fk06ozc/',
'https://ijlselect.recruiterbox.com/jobs/fk01use/',
'https://apsbank.recruiterbox.com/jobs/fk0sm55/',
'https://wingify.recruiterbox.com/jobs/fk0udde/',
'https://mysafehaven.recruiterbox.com/jobs/fk0uy9l',
'https://celtra.recruiterbox.com/jobs/fk0ukc2/',
'https://glptraining.recruiterbox.com/jobs/fk0h7s7',
'https://terrapower.recruiterbox.com/jobs/fk0umv6/',
'https://uken.recruiterbox.com/jobs/447174',
'https://adidevtechnologies.recruiterbox.com/jobs/fk0qk6q/',
'https://greenlightplanet.recruiterbox.com/jobs/fk0swj7/',
'https://sfdigitalservices.recruiterbox.com/jobs/fk0uypg',
'https://eurojob.recruiterbox.com/jobs/fk06kq4/',
'https://mekari.recruiterbox.com/jobs/fk019cj/',
'https://smartwires.recruiterbox.com/jobs/fk0u4k5/',
'https://vagasdb1.recruiterbox.com/jobs/acb6dadc61f847e29fb63a2f200f429e',
'https://myagro.recruiterbox.com/jobs/fk0qadg/',
'https://thegreenehouse.recruiterbox.com/jobs/fk0hw7w/',
'https://praxisga.recruiterbox.com/jobs/fk0q1km/',
'https://entuitive.recruiterbox.com/jobs/fk0up7h/',
'https://adidevtechnologies.recruiterbox.com/jobs/fk0qsmc/',
'https://mysafehaven.recruiterbox.com/jobs/fk0h1r5',
'https://bennington.recruiterbox.com/jobs/fk0uw4r/',
'https://peoplescapehr.recruiterbox.com/jobs/fk0sms3/',
'https://mainebhr.recruiterbox.com/jobs/fk0up3q/',
'https://wolframresearch.recruiterbox.com/jobs/fk0uezp/',
'https://veritaspress.recruiterbox.com/jobs/fk0ulwk/',
'https://njcad.recruiterbox.com/jobs/fk0jq2e',
'https://splashlearn.recruiterbox.com/jobs/fk0u9zy/',
'https://thenovakconsultinggroup.recruiterbox.com/jobs/fk0u851/',
'https://peoplestrata.recruiterbox.com/jobs/fk0u5fo/',
'https://cambridgecomputer.recruiterbox.com/jobs/fk0qt8g/',
'https://softexpert.recruiterbox.com/jobs/fk0udz1/',
'https://oberallc.recruiterbox.com/jobs/fk0qyc5/',
'https://binghamacademy.recruiterbox.com/jobs/fk03cwj/',
'https://mainebhr.recruiterbox.com/jobs/fk0uero/',
'https://sharechat.recruiterbox.com/jobs/fk0upag/',
'https://imagicle.recruiterbox.com/jobs/fk06jhv/',
'https://paccc.recruiterbox.com/jobs/fk0rco/',
'https://linguava.recruiterbox.com/jobs/fk0qpbi',
'https://usydupdate.recruiterbox.com/jobs/fk0hfbx/',
'https://kryptinc.recruiterbox.com/jobs/fk0u556/',
'https://bergmeyer.recruiterbox.com/jobs/fk0u91j/',
'https://asperity.recruiterbox.com/jobs/fk0fk5',
'https://sajenaturalwellnessretail.recruiterbox.com/jobs/fk035ok/',
'https://mixedinkey.recruiterbox.com/jobs/fk01yya/',
'https://flowerchild.recruiterbox.com/jobs/fk0jg5j/',
'https://mercycorpsniger.recruiterbox.com/jobs/fk0sfjp/',
'https://thehenry.recruiterbox.com/jobs/fk0jk17/',
'https://estron.recruiterbox.com/jobs/fk01osv/',
'https://lakepointe.recruiterbox.com/jobs/fk0uyzf/',
'https://develer.recruiterbox.com/jobs/fk0ugzu/',
'https://mekari.recruiterbox.com/jobs/fk0qbly/',
'https://limejump.recruiterbox.com/jobs/fk0u35d/',
'https://mainebhr.recruiterbox.com/jobs/fk0u9wz',
'https://paccc.recruiterbox.com/jobs/fk0cww/',
'https://terrapower.recruiterbox.com/jobs/fk0u4sp/',
'https://digimind.recruiterbox.com/jobs/fk038fx/',
'https://mercycorpsniger.recruiterbox.com/jobs/fk0sm33/',
'https://mainebhr.recruiterbox.com/jobs/fk0u9wr/',
'https://newvoices.recruiterbox.com/jobs/fk0unrn/',
'https://ascellatech.recruiterbox.com/jobs/fk0u321/',
'https://mybankwell.recruiterbox.com/jobs/fk0u8uc/',
'https://vempraglobo.recruiterbox.com/jobs/fk0u868/',
'https://sginnovate.recruiterbox.com/jobs/fk0qbqi/',
'https://givedirectly.recruiterbox.com/jobs/fk0sfce/',
'https://vempraglobo.recruiterbox.com/jobs/fk0qm4v',
'https://hireview.recruiterbox.com/jobs/fk0s6q3/',
'https://moengage.recruiterbox.com/jobs/fk0qlvt/',
'https://mysafehaven.recruiterbox.com/jobs/fk06p4e',
'https://fullerton.recruiterbox.com/jobs/fk0uz6p/',
'https://givedirectly.recruiterbox.com/jobs/fk0ul1m/',
'https://teamomni.recruiterbox.com/jobs/fk03t74/',
'https://mysafehaven.recruiterbox.com/jobs/fk0h3cg',
'https://ocat.recruiterbox.com/jobs/22217',
'https://novigo.recruiterbox.com/jobs/fk0qa19/',
'https://subhiksha.recruiterbox.com/jobs/fk0v1s/',
'https://mybankwell.recruiterbox.com/jobs/fk0usdo/',
'https://testhuset.recruiterbox.com/jobs/fk0fgfm/',
'https://ardentlearninginc.recruiterbox.com/jobs/fk0uy9g/',
'https://vaultconsulting.recruiterbox.com/jobs/fk0jfp1/',
'https://humach.recruiterbox.com/jobs/fk0q9r6',
'https://vantagedatacenters.recruiterbox.com/jobs/fk0uxul',
'https://cambridgecomputer.recruiterbox.com/jobs/fk0uxij',
'https://signeasy.recruiterbox.com/jobs/fk0u3eg/',
'https://fundthatflip.recruiterbox.com/jobs/fk0uy32/',
'https://thequantiumgroup.recruiterbox.com/jobs/fk0u2x2/',
'https://synergenhealth.recruiterbox.com/jobs/fk0hkzk',
'https://vaultconsulting.recruiterbox.com/jobs/fk0ub2i/',
'https://mercycorpsniger.recruiterbox.com/jobs/fk0ukq5/',
'https://stillaguamish.recruiterbox.com/jobs/fk0upc1/',
'https://splashlearn.recruiterbox.com/jobs/fk0u2dn/',
'https://concoconstruction.recruiterbox.com/jobs/fk0jgez/',
'https://novigo.recruiterbox.com/jobs/fk0uvic/',
'https://smartwires.recruiterbox.com/jobs/fk0u5b3/',
'https://myagro.recruiterbox.com/jobs/fk0u4ax/',
'https://mainebhr.recruiterbox.com/jobs/fk0sfeq/',
'https://givedirectly.recruiterbox.com/jobs/fk0shyq/',
'https://culinarydropout.recruiterbox.com/jobs/fk0ent/',
'https://odessainc.recruiterbox.com/jobs/fk0qdys/',
'https://northitalia.recruiterbox.com/jobs/fk035y5/',
'https://uberall.recruiterbox.com/jobs/fk0udkn/',
'https://infolytx.recruiterbox.com/jobs/fk0shz6/',
'https://mybankwell.recruiterbox.com/jobs/fk0u8ul',
'https://flowerchild.recruiterbox.com/jobs/fk06nem/',
'https://funkycorp.recruiterbox.com/jobs/fk03g6b/',
'https://murrayhospital.recruiterbox.com/jobs/fk0ucz3/',
'https://scopicsoftware.recruiterbox.com/jobs/fk0sh7e/',
'https://linkbiz.recruiterbox.com/jobs/fk0uucy/',
'https://nycdatascience.recruiterbox.com/jobs/fk03mmo/',
'https://prempack.recruiterbox.com/jobs/fk03jp3/',
'https://lakepointe.recruiterbox.com/jobs/fk0uy9r/',
'https://janickiindustries.recruiterbox.com/jobs/fk0untu/',
'https://uberall.recruiterbox.com/jobs/fk0ujkt/',
'https://eurasiagroup.recruiterbox.com/jobs/fk0sw2p/',
'https://quanergy.recruiterbox.com/jobs/fk0uou2/',
'https://givedirectly.recruiterbox.com/jobs/fk0s1ec/',
'https://acquisconsulting.recruiterbox.com/jobs/fk0uohx/',
'https://lifepathsystems.recruiterbox.com/jobs/fk0u4tg/',
'https://reside.recruiterbox.com/jobs/fk0swyv/',
'https://aciedge79515.recruiterbox.com/jobs/fk03ml6/',
'https://iristelehealth.recruiterbox.com/jobs/fk0u6bs/',
'https://lakepointe.recruiterbox.com/jobs/fk0uuan/',
'https://reside.recruiterbox.com/jobs/fk0uany/',
'https://verisys.recruiterbox.com/jobs/fk0u5eq/',
'https://greenlightplanet.recruiterbox.com/jobs/fk0uewn/',
'https://celtra.recruiterbox.com/jobs/fk0u2dd/',
'https://mainebhr.recruiterbox.com/jobs/fk0qjpb/',
'https://findingclarity.recruiterbox.com/jobs/fk0u512/',
'https://whatfix101.recruiterbox.com/jobs/fk0qpma/',
'https://humancaresystems.recruiterbox.com/jobs/fk0uabz/',
'https://calibrecpa.recruiterbox.com/jobs/fk0u33p/',
'https://richelieu.recruiterbox.com/jobs/fk0uq4n',
'https://seeq.recruiterbox.com/jobs/fk0u5vg/',
'https://binghamacademy.recruiterbox.com/jobs/fk03chk/',
'https://reside.recruiterbox.com/jobs/fk0u5i2/',
'https://culinarydropout.recruiterbox.com/jobs/fk042e/',
'https://lambda3.recruiterbox.com/jobs/fk01tas/',
'https://ugrowthfund.recruiterbox.com/jobs/fk015sx/',
'https://colcare.recruiterbox.com/jobs/fk0uxzc',
'https://athreon.recruiterbox.com/jobs/fk032fy/',
'https://vantagedatacenters.recruiterbox.com/jobs/fk0ufyl/',
'https://vagasdb1.recruiterbox.com/jobs/fk03z23/',
'https://splashlearn.recruiterbox.com/jobs/fk0ugj9/',
'https://northitalia.recruiterbox.com/jobs/fk0mi59/',
'https://seacoast.recruiterbox.com/jobs/fk0uknp/',
'https://kyosk.recruiterbox.com/jobs/fk0u7f5/',
'https://petroliana.recruiterbox.com/jobs/fk0ubar',
'https://locatee.recruiterbox.com/jobs/fk0ukbx/',
'https://fullerton.recruiterbox.com/jobs/05a1bc3725a943678254bfe3806f47dd',
'https://sajenaturalwellnessretail.recruiterbox.com/jobs/fk0358m/',
'https://mainebhr.recruiterbox.com/jobs/fk0shak/',
'https://colcare.recruiterbox.com/jobs/fk0u9mz',
'https://mekari.recruiterbox.com/jobs/fk01bnt/',
'https://latelieranimation.recruiterbox.com/jobs/fk0f9ls/',
'https://mkdelectric79060.recruiterbox.com/jobs/fk0u776/',
'https://vagasdb1.recruiterbox.com/jobs/fk0sw6e/',
'https://altairsw.recruiterbox.com/jobs/fk0uxqz',
'https://parkwestgallery.recruiterbox.com/jobs/fk0jc36/',
'https://richelieu.recruiterbox.com/jobs/fk0u5ea/',
'https://mekari.recruiterbox.com/jobs/fk0f2j3',
'https://culinarydropout.recruiterbox.com/jobs/fk0enq/',
'https://vagasdb1.recruiterbox.com/jobs/72cd866ec9104e66ae7b96b18c992a2c',
'https://flyersenergy.recruiterbox.com/jobs/fk0ubkg/',
'https://develer.recruiterbox.com/jobs/fk0uljm/',
'https://okhi.recruiterbox.com/jobs/fk0us8s/',
'https://fullerton.recruiterbox.com/jobs/4ac2617cda9a4aaaab8e64a24509dd53',
'https://avaaz.recruiterbox.com/jobs/fk0shr3/',
'https://mysafehaven.recruiterbox.com/jobs/fk0qy1i',
'https://linkbiz.recruiterbox.com/jobs/fk06p25/',
'https://wolframresearch.recruiterbox.com/jobs/fk0u4q9/',
'https://signspecialists.recruiterbox.com/jobs/fk0hsmm',
'https://fuel3d.recruiterbox.com/jobs/fk0uyy5/',
'https://vikingcruises.recruiterbox.com/jobs/fk0sfjg/',
'https://wuyee.recruiterbox.com/jobs/fk0uga1/',
'https://colorofchange.recruiterbox.com/jobs/fk0ub1i/',
'https://rocketsofawesome.recruiterbox.com/jobs/fk0sfpg/',
'https://centraldrugsrx.recruiterbox.com/jobs/fk03wya',
'https://shecan.recruiterbox.com/jobs/fk0uezv',
'https://greytip.recruiterbox.com/jobs/fk0ui3h/',
'https://culinarydropout.recruiterbox.com/jobs/fk0en1/',
'https://limejump.recruiterbox.com/jobs/fk0s6q1/',
'https://mercycorpsniger.recruiterbox.com/jobs/fk0sf8d/',
'https://newvoices.recruiterbox.com/jobs/fk0qg3f/',
'https://subhiksha.recruiterbox.com/jobs/fk0jvcm/',
'https://boardofchildcare.recruiterbox.com/jobs/fk0qq44',
'https://develer.recruiterbox.com/jobs/fk01v6j/',
'https://avaaz.recruiterbox.com/jobs/fk0u5n1/',
'https://givedirectly.recruiterbox.com/jobs/fk0sm81/',
'https://terrapower.recruiterbox.com/jobs/fk0udnc',
'https://celtra.recruiterbox.com/jobs/fk0qlp3/',
'https://fiducial.recruiterbox.com/jobs/fk0swu7/',
'https://vempraglobo.recruiterbox.com/jobs/fk0smms/',
'https://thenovakconsultinggroup.recruiterbox.com/jobs/fk0u522/',
'https://mainebhr.recruiterbox.com/jobs/fk0sfl2/',
'https://mainebhr.recruiterbox.com/jobs/fk0ube5/',
'https://aquilacommercial.recruiterbox.com/jobs/fk0s6nj',
'https://culinarydropout.recruiterbox.com/jobs/fk06ozc/',
'https://ijlselect.recruiterbox.com/jobs/fk01use/',
'https://apsbank.recruiterbox.com/jobs/fk0sm55/',
'https://wingify.recruiterbox.com/jobs/fk0udde/',
'https://mysafehaven.recruiterbox.com/jobs/fk0uy9l',
'https://celtra.recruiterbox.com/jobs/fk0ukc2/',
'https://glptraining.recruiterbox.com/jobs/fk0h7s7',
'https://terrapower.recruiterbox.com/jobs/fk0umv6/',
'https://uken.recruiterbox.com/jobs/447174',
'https://adidevtechnologies.recruiterbox.com/jobs/fk0qk6q/',
'https://greenlightplanet.recruiterbox.com/jobs/fk0swj7/',
'https://sfdigitalservices.recruiterbox.com/jobs/fk0uypg',
'https://eurojob.recruiterbox.com/jobs/fk06kq4/',
'https://mekari.recruiterbox.com/jobs/fk019cj/',
'https://smartwires.recruiterbox.com/jobs/fk0u4k5/',
'https://vagasdb1.recruiterbox.com/jobs/acb6dadc61f847e29fb63a2f200f429e',
'https://myagro.recruiterbox.com/jobs/fk0qadg/',
'https://thegreenehouse.recruiterbox.com/jobs/fk0hw7w/',
'https://praxisga.recruiterbox.com/jobs/fk0q1km/',
'https://entuitive.recruiterbox.com/jobs/fk0up7h/',
'https://adidevtechnologies.recruiterbox.com/jobs/fk0qsmc/',
'https://mysafehaven.recruiterbox.com/jobs/fk0h1r5',
'https://bennington.recruiterbox.com/jobs/fk0uw4r/',
'https://peoplescapehr.recruiterbox.com/jobs/fk0sms3/',
'https://mainebhr.recruiterbox.com/jobs/fk0up3q/',
'https://wolframresearch.recruiterbox.com/jobs/fk0uezp/',
'https://veritaspress.recruiterbox.com/jobs/fk0ulwk/',
'https://njcad.recruiterbox.com/jobs/fk0jq2e',
'https://splashlearn.recruiterbox.com/jobs/fk0u9zy/',
'https://thenovakconsultinggroup.recruiterbox.com/jobs/fk0u851/',
'https://peoplestrata.recruiterbox.com/jobs/fk0u5fo/',
'https://cambridgecomputer.recruiterbox.com/jobs/fk0qt8g/',
'https://softexpert.recruiterbox.com/jobs/fk0udz1/',
'https://oberallc.recruiterbox.com/jobs/fk0qyc5/',
'https://binghamacademy.recruiterbox.com/jobs/fk03cwj/',
'https://mainebhr.recruiterbox.com/jobs/fk0uero/',
'https://sharechat.recruiterbox.com/jobs/fk0upag/',
'https://imagicle.recruiterbox.com/jobs/fk06jhv/',
'https://paccc.recruiterbox.com/jobs/fk0rco/',
'https://linguava.recruiterbox.com/jobs/fk0qpbi',
'https://usydupdate.recruiterbox.com/jobs/fk0hfbx/',
'https://kryptinc.recruiterbox.com/jobs/fk0u556/',
'https://bergmeyer.recruiterbox.com/jobs/fk0u91j/',
'https://asperity.recruiterbox.com/jobs/fk0fk5',
'https://sajenaturalwellnessretail.recruiterbox.com/jobs/fk035ok/',
'https://mixedinkey.recruiterbox.com/jobs/fk01yya/',
'https://flowerchild.recruiterbox.com/jobs/fk0jg5j/',
'https://mercycorpsniger.recruiterbox.com/jobs/fk0sfjp/',
'https://thehenry.recruiterbox.com/jobs/fk0jk17/',
'https://estron.recruiterbox.com/jobs/fk01osv/',
'https://lakepointe.recruiterbox.com/jobs/fk0uyzf/',
'https://develer.recruiterbox.com/jobs/fk0ugzu/',
'https://mekari.recruiterbox.com/jobs/fk0qbly/',
'https://limejump.recruiterbox.com/jobs/fk0u35d/',
'https://mainebhr.recruiterbox.com/jobs/fk0u9wz',
'https://paccc.recruiterbox.com/jobs/fk0cww/',
'https://terrapower.recruiterbox.com/jobs/fk0u4sp/',
'https://digimind.recruiterbox.com/jobs/fk038fx/',
'https://mercycorpsniger.recruiterbox.com/jobs/fk0sm33/',
'https://mainebhr.recruiterbox.com/jobs/fk0u9wr/',
'https://newvoices.recruiterbox.com/jobs/fk0unrn/',
'https://ascellatech.recruiterbox.com/jobs/fk0u321/',
'https://mybankwell.recruiterbox.com/jobs/fk0u8uc/',
'https://vempraglobo.recruiterbox.com/jobs/fk0u868/',
'https://sginnovate.recruiterbox.com/jobs/fk0qbqi/',
'https://okhi.recruiterbox.com/jobs/fk0us8s/',
'https://fullerton.recruiterbox.com/jobs/4ac2617cda9a4aaaab8e64a24509dd53',
'https://avaaz.recruiterbox.com/jobs/fk0shr3/',
'https://mysafehaven.recruiterbox.com/jobs/fk0qy1i',
'https://linkbiz.recruiterbox.com/jobs/fk06p25/',
'https://wolframresearch.recruiterbox.com/jobs/fk0u4q9/',
'https://signspecialists.recruiterbox.com/jobs/fk0hsmm',
'https://fuel3d.recruiterbox.com/jobs/fk0uyy5/',
'https://vikingcruises.recruiterbox.com/jobs/fk0sfjg/',
'https://wuyee.recruiterbox.com/jobs/fk0uga1/',
'https://colorofchange.recruiterbox.com/jobs/fk0ub1i/',
'https://rocketsofawesome.recruiterbox.com/jobs/fk0sfpg/',
'https://centraldrugsrx.recruiterbox.com/jobs/fk03wya',
'https://shecan.recruiterbox.com/jobs/fk0uezv',
'https://greytip.recruiterbox.com/jobs/fk0ui3h/',
'https://culinarydropout.recruiterbox.com/jobs/fk0en1/',
'https://limejump.recruiterbox.com/jobs/fk0s6q1/',
'https://mercycorpsniger.recruiterbox.com/jobs/fk0sf8d/',
'https://newvoices.recruiterbox.com/jobs/fk0qg3f/',
'https://subhiksha.recruiterbox.com/jobs/fk0jvcm/',
'https://boardofchildcare.recruiterbox.com/jobs/fk0qq44',
'https://develer.recruiterbox.com/jobs/fk01v6j/',
'https://avaaz.recruiterbox.com/jobs/fk0u5n1/',
'https://givedirectly.recruiterbox.com/jobs/fk0sm81/',
'https://terrapower.recruiterbox.com/jobs/fk0udnc',
'https://celtra.recruiterbox.com/jobs/fk0qlp3/',
'https://fiducial.recruiterbox.com/jobs/fk0swu7/',
'https://vempraglobo.recruiterbox.com/jobs/fk0smms/',
'https://thenovakconsultinggroup.recruiterbox.com/jobs/fk0u522/',
'https://mainebhr.recruiterbox.com/jobs/fk0sfl2/',
'https://mainebhr.recruiterbox.com/jobs/fk0ube5/',
'https://aquilacommercial.recruiterbox.com/jobs/fk0s6nj',
'https://culinarydropout.recruiterbox.com/jobs/fk06ozc/',
'https://ijlselect.recruiterbox.com/jobs/fk01use/',
'https://apsbank.recruiterbox.com/jobs/fk0sm55/',
'https://wingify.recruiterbox.com/jobs/fk0udde/',
'https://mysafehaven.recruiterbox.com/jobs/fk0uy9l',
'https://celtra.recruiterbox.com/jobs/fk0ukc2/',
'https://glptraining.recruiterbox.com/jobs/fk0h7s7',
'https://terrapower.recruiterbox.com/jobs/fk0umv6/',
'https://uken.recruiterbox.com/jobs/447174',
'https://adidevtechnologies.recruiterbox.com/jobs/fk0qk6q/',
'https://greenlightplanet.recruiterbox.com/jobs/fk0swj7/',
'https://sfdigitalservices.recruiterbox.com/jobs/fk0uypg',
'https://eurojob.recruiterbox.com/jobs/fk06kq4/',
'https://mekari.recruiterbox.com/jobs/fk019cj/',
'https://smartwires.recruiterbox.com/jobs/fk0u4k5/',
'https://vagasdb1.recruiterbox.com/jobs/acb6dadc61f847e29fb63a2f200f429e',
'https://myagro.recruiterbox.com/jobs/fk0qadg/',
'https://thegreenehouse.recruiterbox.com/jobs/fk0hw7w/',
'https://praxisga.recruiterbox.com/jobs/fk0q1km/',
'https://entuitive.recruiterbox.com/jobs/fk0up7h/',
'https://adidevtechnologies.recruiterbox.com/jobs/fk0qsmc/',
'https://mysafehaven.recruiterbox.com/jobs/fk0h1r5',
'https://bennington.recruiterbox.com/jobs/fk0uw4r/',
'https://peoplescapehr.recruiterbox.com/jobs/fk0sms3/',
'https://mainebhr.recruiterbox.com/jobs/fk0up3q/',
'https://wolframresearch.recruiterbox.com/jobs/fk0uezp/',
'https://veritaspress.recruiterbox.com/jobs/fk0ulwk/',
'https://njcad.recruiterbox.com/jobs/fk0jq2e',
'https://splashlearn.recruiterbox.com/jobs/fk0u9zy/',
'https://thenovakconsultinggroup.recruiterbox.com/jobs/fk0u851/',
'https://peoplestrata.recruiterbox.com/jobs/fk0u5fo/',
'https://cambridgecomputer.recruiterbox.com/jobs/fk0qt8g/',
'https://softexpert.recruiterbox.com/jobs/fk0udz1/',
'https://oberallc.recruiterbox.com/jobs/fk0qyc5/',
'https://binghamacademy.recruiterbox.com/jobs/fk03cwj/',
'https://mainebhr.recruiterbox.com/jobs/fk0uero/',
'https://sharechat.recruiterbox.com/jobs/fk0upag/',
'https://imagicle.recruiterbox.com/jobs/fk06jhv/',
'https://paccc.recruiterbox.com/jobs/fk0rco/',
'https://linguava.recruiterbox.com/jobs/fk0qpbi',
'https://usydupdate.recruiterbox.com/jobs/fk0hfbx/',
'https://kryptinc.recruiterbox.com/jobs/fk0u556/',
'https://bergmeyer.recruiterbox.com/jobs/fk0u91j/',
'https://asperity.recruiterbox.com/jobs/fk0fk5',
'https://sajenaturalwellnessretail.recruiterbox.com/jobs/fk035ok/',
'https://mixedinkey.recruiterbox.com/jobs/fk01yya/',
'https://flowerchild.recruiterbox.com/jobs/fk0jg5j/',
'https://mercycorpsniger.recruiterbox.com/jobs/fk0sfjp/',
'https://thehenry.recruiterbox.com/jobs/fk0jk17/',
'https://estron.recruiterbox.com/jobs/fk01osv/',
'https://lakepointe.recruiterbox.com/jobs/fk0uyzf/',
'https://develer.recruiterbox.com/jobs/fk0ugzu/',
'https://mekari.recruiterbox.com/jobs/fk0qbly/',
'https://limejump.recruiterbox.com/jobs/fk0u35d/',
'https://mainebhr.recruiterbox.com/jobs/fk0u9wz',
'https://paccc.recruiterbox.com/jobs/fk0cww/',
'https://terrapower.recruiterbox.com/jobs/fk0u4sp/',
'https://digimind.recruiterbox.com/jobs/fk038fx/',
'https://mercycorpsniger.recruiterbox.com/jobs/fk0sm33/',
'https://mainebhr.recruiterbox.com/jobs/fk0u9wr/',
'https://newvoices.recruiterbox.com/jobs/fk0unrn/',
'https://ascellatech.recruiterbox.com/jobs/fk0u321/',
'https://mybankwell.recruiterbox.com/jobs/fk0u8uc/',
'https://vempraglobo.recruiterbox.com/jobs/fk0u868/',
'https://sginnovate.recruiterbox.com/jobs/fk0qbqi/',
'https://plexinc.recruiterbox.com/jobs',
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