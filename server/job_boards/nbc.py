import requests, json, sys, random
from datetime import datetime
from .modules import create_temp_json
from .modules import headers as h
# import modules.create_temp_json as create_temp_json
# import modules.headers as h


def get_jobs(date: str, url: str, company: str, position: str, location: str):
    data = create_temp_json.data
    post_date = datetime.timestamp(datetime.strptime(str(date), "%m/%d/%Y"))
    
    data.append({
        "timestamp": post_date,
        "title": position,
        "company": company,
        "url": url,
        "location": location,
        "source": company,
        "source_url": "https://www.nbcunicareers.com/careers",
        "category": "job"
    })
    print(f"=> nbcuniversal: Added {position} for {company}")


def get_results(item: str):
    for i in item:
        # try:
        date = i["field_lastupdated"]+"/"+datetime.now().date().strftime("%Y")
        position = i["title"].strip()
        company_name = "NBCUniversal"
        apply_url = i["field_detailurl"].replace("&amp;", "&").strip()
        locations_string = ",".join(i["field_location"].split(",")[::-1]).replace(",United States", "").strip() if len(i["field_location"].split(",")) < 4 else i["field_location"].replace("United States,", "").strip()

        get_jobs(date, apply_url, company_name, position, locations_string)
        # except:
        #     pass

def get_url():
    page = 0
    items = 10

    while items > 0:
        headers = {"User-Agent": random.choice(h.headers)}
        url = f"https://www.nbcunicareers.com/api/brjobs?_format=json&page={page}&profession=1098"
        response = requests.get(url, headers=headers)

        if response.ok:
            data = json.loads(response.text)[0]["rows"]
            get_results(data)
        else:
            print(f"Error. Status Code:", response.status_code)

        page+=1
        items = len(data)


def main():
    get_url()


# main()
# sys.exit(0)