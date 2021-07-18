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
  "https://jobs.ashbyhq.com/deel",
  "https://jobs.ashbyhq.com/Ashby",
  "https://jobs.ashbyhq.com/belvo",
  "https://jobs.ashbyhq.com/veev",
  "https://jobs.ashbyhq.com/Alpaca",
  "https://jobs.ashbyhq.com/found",
  "https://jobs.ashbyhq.com/VanMoof",
  "https://jobs.ashbyhq.com/upandup",
  "https://jobs.ashbyhq.com/memora",
  "https://jobs.ashbyhq.com/mati",
  "https://jobs.ashbyhq.com/treasuryprime",
  "https://jobs.ashbyhq.com/Census",
  "https://jobs.ashbyhq.com/leadiq",
  "https://jobs.ashbyhq.com/hearth",
  "https://jobs.ashbyhq.com/upflow",
  "https://jobs.ashbyhq.com/humaans",
  "https://jobs.ashbyhq.com/kovo",
  "https://jobs.ashbyhq.com/stytch",
  "https://jobs.ashbyhq.com/standard",
  "https://jobs.ashbyhq.com/nextmusic",
  "https://jobs.ashbyhq.com/OctoML",
  "https://jobs.ashbyhq.com/Sketchbox",
  "https://jobs.ashbyhq.com/commsor",
  "https://jobs.ashbyhq.com/bigeye",
  "https://jobs.ashbyhq.com/digisure",
  "https://jobs.ashbyhq.com/Pipeline",
  "https://jobs.ashbyhq.com/zendar",
  "https://jobs.ashbyhq.com/duneanalytics",
  "https://jobs.ashbyhq.com/blankashby1",
  "https://jobs.ashbyhq.com/Aven",
  "https://jobs.ashbyhq.com/teachfx",
  "https://jobs.ashbyhq.com/CMI",
  "https://jobs.ashbyhq.com/safelease",
  "https://jobs.ashbyhq.com/clarisights",
  "https://jobs.ashbyhq.com/correlated",
  "https://jobs.ashbyhq.com/middesk",
  "https://jobs.ashbyhq.com/firstbase",
  "https://jobs.ashbyhq.com/greenskygames",
  "https://jobs.ashbyhq.com/customeracquisition",
  "https://jobs.ashbyhq.com/convictional",
  "https://jobs.ashbyhq.com/impira",
  "https://jobs.ashbyhq.com/latchai",
  "https://jobs.ashbyhq.com/ycombinator",
  "https://jobs.ashbyhq.com/portal",
  "https://jobs.ashbyhq.com/sonalabs",
  "https://jobs.ashbyhq.com/newness",
  "https://jobs.ashbyhq.com/valiu",
  "https://jobs.ashbyhq.com/juked",
  "https://jobs.ashbyhq.com/asaak",
  "https://jobs.ashbyhq.com/bedrockocean",
  "https://jobs.ashbyhq.com/Rocketplace",
  "https://jobs.ashbyhq.com/GordianSoftware",
  "https://jobs.ashbyhq.com/teamtito",
  "https://jobs.ashbyhq.com/juni",
  "https://jobs.ashbyhq.com/stemma",
  "https://jobs.ashbyhq.com/sortly",
  "https://jobs.ashbyhq.com/beeper",
  "https://jobs.ashbyhq.com/EAG",
  "https://jobs.ashbyhq.com/avala",
  "https://jobs.ashbyhq.com/snackpass",
  "https://jobs.ashbyhq.com/Parabola",
  "https://jobs.ashbyhq.com/waitwhile",
  "https://jobs.ashbyhq.com/insight-browser",
  "https://jobs.ashbyhq.com/pledge.earth",
  "https://jobs.ashbyhq.com/unchained.capital",
  "https://jobs.ashbyhq.com/Standard/a11007b5-3b40-4944-b73e-1ce959246fc8",
  "https://jobs.ashbyhq.com/juked/d5a0cc0b-ad79-4cce-85d8-620eaf9b3233",
  "https://jobs.ashbyhq.com/bedrockocean/d274d0ff-547a-4628-a3ef-d9419bba1837",
  "https://jobs.ashbyhq.com/Standard/a97462b2-9e01-4ea3-89e5-6ee22201ed0d",
  "https://jobs.ashbyhq.com/belvo/833bf9f3-5680-4316-9071-7c6327bf6c2c",
  "https://jobs.ashbyhq.com/upflow/1e5b6b3d-de52-4e9d-b8b5-dd1cf5acb74a",
  "https://jobs.ashbyhq.com/teachfx/a0bc0cca-9e4e-42a1-b9d5-be6e626ca443",
  "https://jobs.ashbyhq.com/belvo/b8bf3377-62bc-4596-a46e-e95b8813bdf1",
  "https://jobs.ashbyhq.com/customeracquisition/99d83a14-26ba-4491-bda2-87f6b6b11ff1",
  "https://jobs.ashbyhq.com/searchlight/872d987d-7b3b-4288-b5e4-891024a8628f",
  "https://jobs.ashbyhq.com/Ashby/c5440c85-c5bb-4e7a-b32d-be889955bf67",
  "https://jobs.ashbyhq.com/teachfx/ee989ac9-eb17-4514-a5ca-798893f0412b",
  "https://jobs.ashbyhq.com/bigeye/7d50e2e5-3931-4730-a89c-013a712a8ced",
  "https://jobs.ashbyhq.com/searchlight/db796b13-404e-47e9-9ff8-9ae3fe7537b3",
  "https://jobs.ashbyhq.com/bedrockocean/5df93077-9b7d-40ae-ba7d-215fa12dfdd1",
  "https://jobs.ashbyhq.com/juked/15c349f1-d84d-4f7d-8246-49eae8cd91d1",
  "https://jobs.ashbyhq.com/Aven/a8aee54b-cd52-4d87-bd9a-eb43a1d3557f",
  "https://jobs.ashbyhq.com/moderntreasury/0090e8d7-cb53-4517-98c9-6c3c12b77e18",
  "https://jobs.ashbyhq.com/Aven/ac3d0a19-b692-4995-864c-f47aa2ab71dd",
  "https://jobs.ashbyhq.com/veev/66cc9b18-4a4c-4972-9f9f-4fb78590779b",
  "https://jobs.ashbyhq.com/dotconnect/1ef0f569-bbf5-4729-a9ac-dca50e145cf4",
  "https://jobs.ashbyhq.com/Cartloop/645181c0-4b2f-412f-b18a-d23939f1553f",
  "https://jobs.ashbyhq.com/bigeye/ec71c435-2adf-4be1-b64d-e3772e1347fa",
  "https://jobs.ashbyhq.com/middesk/dacf2ba3-b03f-4242-8722-15478c35e123",
  "https://jobs.ashbyhq.com/memora/ab4b3892-6a15-42e4-b18c-8b53696aad23",
  "https://jobs.ashbyhq.com/bigeye/328b8f74-00ae-4e91-b086-92d8bddb32fc",
  "https://jobs.ashbyhq.com/searchlight/b524b5b1-4751-44a8-867b-1645d80befad",
  "https://jobs.ashbyhq.com/bedrockocean/ca8f6e3c-c74d-4098-87f3-0e5a57ea9449",
  "https://jobs.ashbyhq.com/convictional/2ae9c598-8333-4cb3-b2b5-5443b809865d",
  "https://jobs.ashbyhq.com/ashby/746da12d-6bd4-4ea7-9279-a032770a2d21",
  "https://jobs.ashbyhq.com/bigeye/45cbe5e5-4fbb-4038-81c5-639bd424f6f3",
  "https://jobs.ashbyhq.com/middesk/ccc5d49a-bdb0-4faa-9fd2-297d7e6a2fb9",
  "https://jobs.ashbyhq.com/OctoML/c7559d59-1af7-41ba-bbcd-d09e668870b0",
  "https://jobs.ashbyhq.com/belvo/9ad0d4d9-8831-4f5a-8089-ac559c778793",
  "https://jobs.ashbyhq.com/nextmusic/ccf57b53-37db-43f9-bf9c-f5101d4253d2",
  "https://jobs.ashbyhq.com/middesk/de09ba62-5ee4-4170-bdd2-a5900bbd6edf",
  "https://jobs.ashbyhq.com/belvo/4bb0b898-a6e2-4362-bd3c-3c6f481fdf4e",
  "https://jobs.ashbyhq.com/upflow/b8c84fd6-f1c8-4e7f-be52-069d40737571",
  "https://jobs.ashbyhq.com/Aven/78aad618-127e-424c-9acc-49b58197acfb",
  "https://jobs.ashbyhq.com/Aven/ac7016b3-1a60-4ef8-a22e-a9dd9e7c5a0e",
  "https://jobs.ashbyhq.com/Cartloop/fa9402e4-526f-4661-ad84-0590f2b18861",
  "https://jobs.ashbyhq.com/Cartloop/8633c62e-157e-457b-b696-fdc3e38b2cc4",
  "https://jobs.ashbyhq.com/OctoML/16ab7270-913b-4af2-bedc-3683eb3afa5b",
  "https://jobs.ashbyhq.com/memora/248fd9b3-8491-41af-aafc-4624e1413f24",
  "https://jobs.ashbyhq.com/standard/43aa120b-fbc6-4a61-9139-1ef95be08233",
  "https://jobs.ashbyhq.com/Standard/5dada9ef-630c-425a-bc3d-70492ba5c852",
  "https://jobs.ashbyhq.com/rootine/0856474a-d43d-49b7-b41d-01c06e99d2a0",
  "https://jobs.ashbyhq.com/Cartloop/6ac01beb-134f-4faa-983e-1f7b33389b2d",
  "https://jobs.ashbyhq.com/Cartloop/68ec412b-4caf-49c9-9c4a-83cb87052727",
  "https://jobs.ashbyhq.com/teamtito/4e6541ed-9102-47ec-bb54-73a833f1b7f2",
  "https://jobs.ashbyhq.com/Aven/97f7fba4-4112-4366-9841-c7e87c5983c0",
  "https://jobs.ashbyhq.com/Convictional/9ce18823-de30-40ae-8f72-0e636680763d",
  "https://jobs.ashbyhq.com/Ashby/3aee80da-4b17-46eb-bfc5-85b59ef850da",
  "https://jobs.ashbyhq.com/searchlight/59ff9885-6217-4b1e-9ce2-65c77119e84b",
  "https://jobs.ashbyhq.com/Ashby/d33a04db-7383-4c53-9c5d-b1828b18dbe6",
  "https://jobs.ashbyhq.com/belvo/5e417f94-ef49-4d52-a3b6-3b4b4b0e44f2",
  "https://jobs.ashbyhq.com/modernfertility/ec972c70-7c20-4608-9a84-ecdcc129b17d",
  "https://jobs.ashbyhq.com/clarisights/f39c8756-5f66-463e-9485-c7f83a0c8778",
  "https://jobs.ashbyhq.com/upflow/a0dd54c1-4249-4f0d-998b-4a858b4c4118",
  "https://jobs.ashbyhq.com/hearth/dc6d0abd-49ec-49de-ae63-191755e96b75",
  "https://jobs.ashbyhq.com/bigeye/79f4dd96-4be2-4e99-8f4b-32aa5ba63667",
  "https://jobs.ashbyhq.com/firstbaseio/469b6b2a-bba3-4ded-894f-241ca1a58545",
  "https://jobs.ashbyhq.com/modernfertility/6cb87b0a-79a7-4979-b963-9c4363ae1dae",
  "https://jobs.ashbyhq.com/nudgetext/1e2784f1-1b48-4a6b-937a-f6418e17a713",
  "https://jobs.ashbyhq.com/Alpaca/41616dcc-a2d3-47ac-a250-c266148d4318",
  "https://jobs.ashbyhq.com/leadiq/09d472ba-9c61-44de-8485-91b96745c560",
  "https://jobs.ashbyhq.com/stemma/2fed48b7-3969-4e5e-b1c5-4cab21e7213e",
  "https://jobs.ashbyhq.com/moderntreasury/43e8b3b6-605f-4c9a-8237-140a7d39e4b9",
  "https://jobs.ashbyhq.com/Aven/8b3c7a50-bf72-430a-a33a-6cf8ac90cf91",
  "https://jobs.ashbyhq.com/middesk/89482392-56fe-452a-8960-a743d0f02f9a",
  "https://jobs.ashbyhq.com/valiu/33e21cc3-039c-4dc4-82b8-c1a496ad6d8e",
  "https://jobs.ashbyhq.com/nudgetext/eb207e0a-0612-4aac-a440-7a46c0a09b1c",
  "https://jobs.ashbyhq.com/commsor/d7feccab-0eb3-4910-81fd-6d8c359d1f8e",
  "https://jobs.ashbyhq.com/veev/9cff5975-ea96-4803-9117-64a16584c474",
  "https://jobs.ashbyhq.com/Cartloop/ffff02af-2a5b-4764-8e09-48a7bddddef3",
  "https://jobs.ashbyhq.com/blankashby1/7e10499f-f6be-42bb-b3f4-8eb6e6fec5ed",
  "https://jobs.ashbyhq.com/belvo/a8688c02-16ff-471b-b516-65b6dcb64856",
  "https://jobs.ashbyhq.com/clarisights/be80db1b-baf8-44c8-855b-2df11ef5b7f5",
  "https://jobs.ashbyhq.com/veev/09321aa9-3804-4455-8df2-e589e6bcbd05",
  "https://jobs.ashbyhq.com/deel/320cf4cc-5d63-4d7f-8bd4-6bbf515e3e0b",
  "https://jobs.ashbyhq.com/juked/62a2cc19-051f-4bbd-bba7-d9279df151cb",
  "https://jobs.ashbyhq.com/belvo/5e2677c8-3a08-4bf5-b77d-902563d88c89",
  "https://jobs.ashbyhq.com/moderntreasury/b42fbebd-f2be-4bfc-b499-51e1f1184c3f",
  "https://jobs.ashbyhq.com/belvo/cb925a09-a85e-4f83-9ff0-f94071b104d6",
  "https://jobs.ashbyhq.com/searchlight/74d0b2e1-d1ec-4a38-9931-ced7d2f946c1",
  "https://jobs.ashbyhq.com/belvo/b8b2620f-249b-4378-af80-f9b5cc072cac",
  "https://jobs.ashbyhq.com/juked/ab3b4d29-cda0-4593-839a-874b2397d9e8",
  "https://jobs.ashbyhq.com/Cartloop/f721a979-ba68-474f-ac31-df47f7524f1c",
  "https://jobs.ashbyhq.com/memora/97286372-94a9-4d28-a1fe-164e19dcd759",
  "https://jobs.ashbyhq.com/Cartloop/60475160-2363-4cbd-aaa8-6ac907d2c01f",
  "https://jobs.ashbyhq.com/nextmusic/3de82fa0-0c24-47b1-aff5-6eb64ec00410",
  "https://jobs.ashbyhq.com/modernfertility/ca7a62bf-e2c6-492e-a342-b80790942dd9",
  "https://jobs.ashbyhq.com/Cartloop/a1f19709-2ebe-4745-bce0-fbc3c8889e48",
  "https://jobs.ashbyhq.com/hightouch/7f302222-2e06-4e37-8766-87b3bf6068e6",
  "https://jobs.ashbyhq.com/memora/2eefabcc-b9df-45aa-9caa-bce379aa03f1",
  "https://jobs.ashbyhq.com/nextmusic/023f4762-19d1-4679-9625-77cac29ad3ad",
  "https://jobs.ashbyhq.com/nextmusic/d27d6384-b4e0-43c7-933a-05f7df72c65b",
  "https://jobs.ashbyhq.com/Deel/b26d388c-fda6-47a2-a4b0-33f18f983269",
  "https://jobs.ashbyhq.com/blankashby2/821d3ec1-cfba-4416-ab5e-03bca1855951",
  "https://jobs.ashbyhq.com/hearth/dce46bb3-999e-434b-8636-fa29044faa85",
  "https://jobs.ashbyhq.com/nudgetext/271ad7b1-61b2-4a30-8042-2b0fdc8a5fc1",
  "https://jobs.ashbyhq.com/Deel/c5c17aa7-7b7a-4515-af00-85cbc4730514",
  "https://jobs.ashbyhq.com/transform/b1d201ec-8009-4a53-9e9c-927389934d08",
  "https://jobs.ashbyhq.com/memora/ad42e31a-ecc0-49c7-ac76-44f369605072",
  "https://jobs.ashbyhq.com/transform/c07d1b9b-d32c-4397-ae5c-084ccc8a063e",
  "https://jobs.ashbyhq.com/memora/b04acfc7-6eed-4028-a632-5b726b8f6ab8",
  "https://jobs.ashbyhq.com/upflow/0cba4c59-b0c8-447d-b5d7-4085995dc022",
  "https://jobs.ashbyhq.com/veev/ec8c1716-c459-489b-b4d4-709f70b42355",
  "https://jobs.ashbyhq.com/Census/86ddb238-a334-4bdc-815f-e1947732b195",
  "https://jobs.ashbyhq.com/portal/fd51ef78-0c26-41ef-b0a6-4e8b0ae18f37",
  "https://jobs.ashbyhq.com/Cartloop/00129094-8980-48b1-9478-4a575d220266",
  "https://jobs.ashbyhq.com/modernfertility/b24f913e-d2a4-4b03-85c1-3019efcd6c71",
  "https://jobs.ashbyhq.com/veev/8171e51f-9079-4745-9e50-8b2878fe3798",
  "https://jobs.ashbyhq.com/memora/2a1babff-99b0-42fd-8215-c649388a11e0",
  "https://jobs.ashbyhq.com/fieldguide/170b46c3-3157-49c6-b8cf-db87800e1409",
  "https://jobs.ashbyhq.com/Deel/8f89ebc8-d77f-4daa-9b38-88a5ae586f63",
  "https://jobs.ashbyhq.com/memora/a1b9a289-778b-4d2c-8395-dd68c69686b3",
  "https://jobs.ashbyhq.com/OctoML/f4fb38e7-745f-43bf-a3f1-cb86b91b90ec",
  "https://jobs.ashbyhq.com/Aven/85439f3d-66e1-43f8-a3cd-45cd404bdd6a",
  "https://jobs.ashbyhq.com/memora/f7a69454-153c-4a7c-899d-8bccf4ef76a5",
  "https://jobs.ashbyhq.com/Cartloop/559a7de1-eb6e-4dad-8b3b-b01fba9226b8",
  "https://jobs.ashbyhq.com/leadiq/c8da9b85-cb62-41b7-9a0a-9656971fca39",
  "https://jobs.ashbyhq.com/bigeye/7e611f5b-7874-445c-a402-fc634b694b81",
  "https://jobs.ashbyhq.com/standard/b1f12f6e-88aa-49fb-8a4d-2dfed4be19b0",
  "https://jobs.ashbyhq.com/nudgetext/d83fac9d-52f7-431c-afe5-4fae5e11b5fb",
  "https://jobs.ashbyhq.com/veev/4c6d8e13-e472-4f8d-9ec3-055c88f5f0b1",
  "https://jobs.ashbyhq.com/bigeye/a470657d-1833-499d-b558-cb6f59ce2841",
  "https://jobs.ashbyhq.com/Deel/bf960459-2fc0-467b-8e0f-f9e6fcd66c40",
  "https://jobs.ashbyhq.com/deel/151c714b-62d0-4c85-9c2d-32735fd0a7b8",
  "https://jobs.ashbyhq.com/Cartloop/2cb382a7-dab5-4ef6-9842-d9e7f12ae228",
  "https://jobs.ashbyhq.com/memora/1fa4ad49-ca78-49c1-ab10-0159f3177bac",
  "https://jobs.ashbyhq.com/modernfertility/a2470554-ba8b-4a51-a0d5-8d232f5b672c",
  "https://jobs.ashbyhq.com/memora/ccbb11d8-904b-474e-bc3f-138e54342a7f",
  "https://jobs.ashbyhq.com/nudgetext/d7be2b03-49af-458a-9641-e03ade1b6cf2",
  "https://jobs.ashbyhq.com/Ashby/51411d51-18b8-4409-8396-2df04d3c8d63",
  "https://jobs.ashbyhq.com/humaans/af5e8675-387d-4033-8286-ff573e006ef6",
  "https://jobs.ashbyhq.com/memora/0a818da6-ec68-4388-ae08-ddbbade49204",
  "https://jobs.ashbyhq.com/bigeye/cfcc074c-c278-492d-9fc9-8140f7589558",
  "https://jobs.ashbyhq.com/moderntreasury/51bb3f53-b9fb-44d3-bddb-d91cf638df92",
  "https://jobs.ashbyhq.com/moderntreasury/42c661f1-98bf-4254-8d74-a32d9d8f20e8",
  "https://jobs.ashbyhq.com/duneanalytics/9d95b697-af58-421d-b6fd-bad855556c72",
  "https://jobs.ashbyhq.com/octoml/248d8b11-da4d-46be-9b47-0148812ba040",
  "https://jobs.ashbyhq.com/leadiq/636559d6-dce5-4ca0-9d49-ee6c3880625b",
  "https://jobs.ashbyhq.com/leadiq/fb1c49e7-94bc-4eef-93dc-0d41030fcf1f",
  "https://jobs.ashbyhq.com/deel/1ddba069-7835-4feb-9758-e037b8f7ac9c",
  "https://jobs.ashbyhq.com/treasuryprime/95abd3ee-776e-47a5-8640-b3d14cdb37e7",
  "https://jobs.ashbyhq.com/upflow/816a377c-c3ea-4f0b-a2e5-c98407b6edc5",
  "https://jobs.ashbyhq.com/bedrockocean/0f5593bb-c697-45be-a25b-0b070ca9827e",
  "https://jobs.ashbyhq.com/searchlight/336b0b4a-07b9-49c4-a395-8b6083bfa9ec",
  "https://jobs.ashbyhq.com/Deel/c194256f-1958-4ca6-ad25-9ecac95accaf",
  "https://jobs.ashbyhq.com/memora/220e9320-db7a-4fd6-aee0-4e20b0c3230b",
  "https://jobs.ashbyhq.com/bedrockocean/d834aa29-143a-4991-9599-d8b7720ee3fd",
  "https://jobs.ashbyhq.com/found/d9fb3dd7-ad12-4fb2-b0af-bedbff1b3a62",
  "https://jobs.ashbyhq.com/scalemath/c7122e3f-60e9-4e4a-b7e4-91a41ef1ffc3",
  "https://jobs.ashbyhq.com/nextmusic/66d8082e-995c-476a-a268-8369626a209b",
  "https://jobs.ashbyhq.com/digisure/c9b9058f-e3a7-486d-86a0-0c2dadcaa8b7",
  "https://jobs.ashbyhq.com/VanMoof/edcef979-b7d5-4682-a57d-b6060263a90f",
  "https://jobs.ashbyhq.com/veev/adfdf24a-fea9-47c4-b610-386124d86972",
  "https://jobs.ashbyhq.com/bigeye/cb027c04-94ae-41af-831c-4a4bfbe15e43",
  "https://jobs.ashbyhq.com/clarisights/eed444d5-f538-43f0-91b2-c1b6ad913a81",
  "https://jobs.ashbyhq.com/deel/e53ee2c0-7a1b-4b36-894a-2737054fb2f5",
  "https://jobs.ashbyhq.com/clarisights/c701fd1d-30e0-4b92-b02e-0da28db8c1c5",
  "https://jobs.ashbyhq.com/Deel/95a01831-3894-43af-87a8-660963f59c9f",
  "https://jobs.ashbyhq.com/moderntreasury/c986bcac-de5a-4885-acb1-59dfc810d967",
  "https://jobs.ashbyhq.com/memora/b4498a6a-b445-4264-8829-eee559df1b1e",
  "https://jobs.ashbyhq.com/monad/29aa7c0e-adf0-422e-862e-b4b1d6428852",
  "https://jobs.ashbyhq.com/moderntreasury/640c2aca-5a23-4762-b022-27039bd049cf",
  "https://jobs.ashbyhq.com/kolena/06137b1f-9bb6-465c-a998-d8403cb12b10",
  "https://jobs.ashbyhq.com/treasuryprime/9b9fee1e-7eca-4208-b4ef-e991fee9205d",
  "https://jobs.ashbyhq.com/searchlight/981cc6f3-4a53-4523-a02a-aa4666805ca1",
  "https://jobs.ashbyhq.com/digisure/7bb66f10-4864-4b3e-8e58-4d732ca7a3c7",
  "https://jobs.ashbyhq.com/veev/dc946013-9f77-481b-bc0a-45e46fa620bc",
  "https://jobs.ashbyhq.com/bigeye/6562d4a3-ec5d-4a85-978c-03a8a8369ae9",
  "https://jobs.ashbyhq.com/duneanalytics/c8eb493c-e952-472e-a7c2-dc3d0e277421",
  "https://jobs.ashbyhq.com/nextmusic/530891ea-ec74-494c-a584-7d83e1838485",
  "https://jobs.ashbyhq.com/memora/f1089538-42cb-444a-9aa9-6e22d9dcc26e",
  "https://jobs.ashbyhq.com/belvo/5f235ec9-6e1d-4ce2-a775-4824a66b63a7",
  "https://jobs.ashbyhq.com/mati/ea5bb64f-f834-430b-b472-6f8d55eaf72b",
  "https://jobs.ashbyhq.com/belvo/89ea8349-55b5-44e9-93a5-7c859279c631",
  "https://jobs.ashbyhq.com/treasuryprime/1b2a9051-bae1-42a3-b8cf-ffb47f5cc3b5",
  "https://jobs.ashbyhq.com/Pipeline/1d532ad6-3700-4ac5-8b64-28ef5f46b6c9",
  "https://jobs.ashbyhq.com/deel/6057bf56-feea-4406-a830-c39bcc5b9552",
  "https://jobs.ashbyhq.com/upflow/2d7bb900-9fa4-412d-9a67-e94dc2fb01e9",
  "https://jobs.ashbyhq.com/belvo/a51bf754-fc4e-4576-99a6-adb112a73859",
  "https://jobs.ashbyhq.com/belvo/08425968-5a4b-49d2-bc7d-fac950e9ca1c",
  "https://jobs.ashbyhq.com/veev/bdb109f4-0515-432b-8d96-7d8b597cbbd8",
  "https://jobs.ashbyhq.com/Standard/747cf8e5-1e5f-41b2-895a-de37811576cf",
  "https://jobs.ashbyhq.com/transform/24ad0c0e-6afd-4ba7-a3e9-5487745eaaf4",
  "https://jobs.ashbyhq.com/bedrockocean/a8f11d45-6128-4d46-a833-506b9c97789b",
  "https://jobs.ashbyhq.com/veev/3f55c396-060c-44c1-bbba-259aa48c61cf",
  "https://jobs.ashbyhq.com/Deel/3d245177-6178-4670-a36b-72818558dcdf",
  "https://jobs.ashbyhq.com/OctoML/4a84f36b-6c19-423a-98bf-e50918742d52",
  "https://jobs.ashbyhq.com/upandup/48851f50-da0a-4aa8-9c73-e84ab75bf9fe",
  "https://jobs.ashbyhq.com/monad/a9398084-c3b6-43b2-ac98-f6a46b2293fc",
  "https://jobs.ashbyhq.com/Deel/236ce85d-f805-4eb2-a464-f3d1864fb724",
  "https://jobs.ashbyhq.com/Deel/da44ddf2-e159-4457-948f-e6e8208fdce3",
  "https://jobs.ashbyhq.com/modernfertility/71efb6da-e40d-4662-85e0-2dee1dff2335",
  "https://jobs.ashbyhq.com/deel/a247c103-a6a9-4978-8580-66ea954fa47f",
  "https://jobs.ashbyhq.com/hearth/f8726c26-bdaf-4fd4-9d9e-dc8ff1fcfc11",
  "https://jobs.ashbyhq.com/VanMoof/52d74e17-0970-4a02-8437-f3a8ac96a095",
  "https://jobs.ashbyhq.com/commsor/2085679c-08f6-4dcb-a1ec-05e57f22e06e",
  "https://jobs.ashbyhq.com/convictional/fe9f413e-90bf-40f7-a223-6523f8abd4de",
  "https://jobs.ashbyhq.com/Deel/1faf76d5-a5a0-4349-8a18-950469248d59",
  "https://jobs.ashbyhq.com/deel/ca83c489-321e-424b-9931-c4a50f9f50a4",
  "https://jobs.ashbyhq.com/Cartloop/e6d9164e-525a-426b-a50c-eea9c78c4cb5",
  "https://jobs.ashbyhq.com/Deel/0008b7d5-663e-4e96-a56c-15317b8d9d0a",
  "https://jobs.ashbyhq.com/Cartloop/3829a7ef-e56c-4e4b-bffc-57579473cfd8",
  "https://jobs.ashbyhq.com/Alpaca/7d7b6169-a64a-4f67-bbf8-d9156ea3f5f6",
  "https://jobs.ashbyhq.com/deel/777c33d8-7712-4796-86d7-cdbb4ffaf4dc",
  "https://jobs.ashbyhq.com/Cartloop/9a945738-2236-4c88-8183-b2132f5aa0cf",
  "https://jobs.ashbyhq.com/nextmusic/39087dce-29ad-4cd8-bf42-0923fc2284dd",
  "https://jobs.ashbyhq.com/impira/8f2be87a-7c3d-4201-845f-0a24cf650acc",
  "https://jobs.ashbyhq.com/Alpaca/74460793-2ace-4af2-bee0-c96630752222",
  "https://jobs.ashbyhq.com/duneanalytics/147b438c-26f1-46ca-8173-708931a55f85",
  "https://jobs.ashbyhq.com/memora/5a847163-5c0e-41a4-b534-8fee00da0f61",
  "https://jobs.ashbyhq.com/upandup/4a1e1fd0-f67d-4f46-b1de-94d3aacc9784",
  "https://jobs.ashbyhq.com/VanMoof/59581350-4025-44f8-8084-aea63ae886e4",
  "https://jobs.ashbyhq.com/memora/53ce0d9e-0e0e-411e-b1fe-e0c80487aa1e",
  "https://jobs.ashbyhq.com/kovo/381cd3af-083d-4103-9174-b3d4b170e63a",
  "https://jobs.ashbyhq.com/Census/15d26836-4603-4b1f-87d5-8c9f101311e3",
  "https://jobs.ashbyhq.com/Deel/2634abd6-937a-4c7b-a9e1-74574a8181ef",
  "https://jobs.ashbyhq.com/monad/8cfe8fa1-a951-4899-bb2a-63fe4b0919a9",
  "https://jobs.ashbyhq.com/Deel/1643d14e-7153-4203-8a6b-7fec4cab6588",
  "https://jobs.ashbyhq.com/memora/b2a6cda5-d700-41ea-88c6-2317e9506348",
  "https://jobs.ashbyhq.com/moderntreasury/82d5a6d6-ba07-488b-815c-70d00912db0f"
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