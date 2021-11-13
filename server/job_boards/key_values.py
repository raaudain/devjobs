import requests, sys, time, random
from bs4 import BeautifulSoup
from datetime import datetime
from .modules import create_temp_json
from .modules import update_key_values
from .modules import headers as h
# import modules.create_temp_json as create_temp_json
# import modules.update_key_values as update_key_values
# import modules.headers as h


def get_jobs(item: list):
    data = create_temp_json.data
    scraped = create_temp_json.scraped

    exclude = set()
    exclude.add("See All Open Jobs")
    exclude.add("See All Open Roles")
    exclude.add("Interested in joining?")
    exclude.add("All Jobs at CareGuide")
    exclude.add("See All Job Openings")
    exclude.add("See All Open Positions")
    exclude.add("")

    for job in item:
        date = datetime.strftime(datetime.now(), "%Y-%m-%d")
        title = job.find("p", {"class": "open-position--job-title"}).text
        company = job.find("a")["data-company"]
        url = job.find("a", href=True)["href"]
        location = job.find("div", {"class": "open-position--job-information"}).find_all("p")[0].text

        post_date = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d"))

        if title not in exclude and url not in scraped and company not in scraped:
            data.append({
                "timestamp": post_date,
                "title": title,
                "company": company,
                "url": url,
                "location": location,
                "source": "Key Values",
                "source_url": "https://www.keyvalues.com",
                "category": "job"
            })
            scraped.add(url)
            print(f"=> key_values: Added {title} for {company}")
        else:
            print(f"=> key_values: Already scraped {title} for {company}")


def get_results(item: str):
    soup = BeautifulSoup(item, "lxml")
    results = soup.find_all("div", {"class": "open-position-item-contents"})
    get_jobs(results)


def get_url(params: list):
    for param in params:
        headers = {"User-Agent": random.choice(h.headers)}
        url = f"https://www.keyvalues.com{param}"
        response = requests.get(url, headers=headers)

        if response.ok: get_results(response.text)
        else: print(f"=> key_values: Error. Status code:", response.status_code)

        time.sleep(2)


def main():
    f = open(f"./data/params/key_values.txt", "r")
    params = [param.strip() for param in f]
    f.close()

    update_key_values.main()
    get_url(params)


# main()
# sys.exit(0)