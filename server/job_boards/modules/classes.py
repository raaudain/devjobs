from os.path import isfile
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests
import random
from . import create_temp_json
# import modules.create_temp_json as create_temp_json
# import headers as h
# import proxies as p


class Get:
    def __init__(self, url: str):
        self.url = url
        # self.headers = headers

    def response(self):
        url = self.url

        headers = {"User-Agent": random.choice(h.headers)}
        request = requests.Session()
        request.proxies.update(p.proxies)
        response = request.get(url, headers=headers)

        return response

import random

class List_Of_Companies:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def read_file(self):
        file_path = self.file_path
        f = open(file_path, "r")
        companies = [company.strip() for company in f]
        f.close()
        random.shuffle(companies)
        return companies


class Page_Not_Found:
    def __init__(self, file_path: str, param: str):
        self.file_path = file_path
        self.param = param

    def remove_not_found(self):
        file_path = self.file_path
        param = self.param
        f = open(file_path, "r+")
        params = [param.strip() for param in f]
        f.truncate(0)
        f.close()
        file = open(file_path, "w")
        error = open("./data/params/404.txt", "a")
        for p in params:
            if p != param:
                file.write(p+"\n")
            else:
                error.write(p+"\n")
        file.close()
        error.close()


class Filter_Jobs:
    def __init__(self, posting: list):
        self.posting = posting

    def filter(self):
        posting = self.posting
        data = create_temp_json.data
        scraped = create_temp_json.scraped
        title = posting["title"]
        company = posting["company"]
        if ("Engineer" in title or "Data" in title or "IT " in title or "Tech" in title or "Support" in title or "Programmer" in title or "Develover" in title) and ("Electrical" not in title and "HVAC" not in title and "Mechnical" not in title):
            data.append(posting)
            scraped.add(company)
            print(f"=> {posting['source_url']}: Added {title} for {company}")

class Handle_Jobs:
    def __init__(self, date: str, apply_url: str, company_name: str, position: str, location: str, source: str, source_url: str, job_board: str):
        self.date = date
        self.apply_url = apply_url
        self.company_name = company_name
        self.position = position
        self.location = location
        self.source = source
        self.source_url = source_url
        self.job_board = job_board

    def add_job(self):
        data = Create_JSON.data
        scraped = Create_JSON.scraped

        post_date = datetime.timestamp(
            datetime.strptime(str(self.date), "%Y-%m-%d"))

        if self.apply_url not in scraped:
            data.append({
                "timestamp": post_date,
                "title": self.position,
                "company": self.company_name,
                "url": self.apply_url,
                "location": self.location,
                "source": self.source,
                "source_url": self.source_url,
            })
            scraped.add(self.company_name)
            scraped.add(self.apply_url)
            print(
                f"=> {self.job_board}: Added {self.position} for {self.company_name}")

    def add_job_filtered_by_date(self):
        data = Create_JSON.data
        scraped = Create_JSON.scraped

        age = datetime.timestamp(datetime.now() - timedelta(days=30))
        post_date = datetime.timestamp(
            datetime.strptime(str(self.date), "%Y-%m-%d"))

        if self.apply_url not in scraped and age <= post_date and self.company_name not in scraped:
            data.append({
                "timestamp": post_date,
                "title": self.position,
                "company": self.company_name,
                "url": self.apply_url,
                "location": self.location,
                "source": self.source,
                "source_url": self.source_url,
            })
            scraped.add(self.apply_url)
            print(
                f"=> {self.job_board}: Added {self.position} for {self.company_name}")

    def add_job_filtered_by_company_name(self):
        data = Create_JSON.data
        scraped = Create_JSON.scraped

        age = datetime.timestamp(datetime.now() - timedelta(days=30))
        post_date = datetime.timestamp(
            datetime.strptime(str(self.date), "%Y-%m-%d"))

        if self.apply_url not in scraped and age <= post_date:
            data.append({
                "timestamp": post_date,
                "title": self.position,
                "company": self.company_name,
                "url": self.apply_url,
                "location": self.location,
                "source": self.source,
                "source_url": self.source_url,
            })
            scraped.add(self.company_name)
            scraped.add(self.apply_url)
            print(
                f"=> {self.job_board}: Added {self.position} for {self.company_name}")


class Update_Key_Values:

    def filter_companies():
        if isfile("./data/params/key_values.txt"):
            print("=> key_values: Deleting old parameters")
            t = open(f"./data/temp/temp_data.json", "r+")
            t.truncate(0)
            t.close()
        url = "https://www.keyvalues.com/"
        html = requests.get(url).text
        soup = BeautifulSoup(html, "lxml")
        company = open("./data/params/key_values.txt", "w")
        links = soup.find_all("a", {"class": "thumbnail-link"}, href=True)
        f = open("./data/params/key_values_unwanted.txt")
        unwanted = [w.strip() for w in f]
        f.close()
        for link in links:
            if link["href"] not in unwanted:
                company.write(link["href"]+"\n")
        print("=> key_values: Updated parameters")
        company.close()


class Create_JSON:
    data = []
    scraped = set()

    def create_temp_file(data):
        temp = "./data/temp/temp_data.json"
        if isfile(temp):
            print("=> temp_data.json: Deleting old content")
            t = open(temp, "r+")
            t.truncate(0)
            t.close()
        with open(temp, "a", encoding="utf-8") as file:
            print("=> temp_data.json: Generating new content")
            json.dump(data, file, ensure_ascii=False, indent=4)

    def create_file():
        temp = "./data/temp/temp_data.json"
        f = open(temp)
        data = json.load(f)
        f.close()
        main = "./data/data.json"
        if isfile(main):
            print("=> data.json: Deleting old content")
            t = open(main, "r+")
            t.truncate(0)
            t.close()
        ordered_data = sorted(data, key=lambda i: i["timestamp"], reverse=True)
        with open(main, "a", encoding="utf-8") as file:
            print("=> data.json: Generating new content")
            json.dump(ordered_data, file, ensure_ascii=False, indent=4)


class Create_Temp_JSON:
    data = []
    scraped = set()

    def create_temp_file(self):
        temp = "./data/temp/temp_data.json"
        if isfile(temp):
            print("=> temp_data.json: Deleting old content")
            t = open(temp, "r+")
            t.truncate(0)
            t.close()
        with open(temp, "a", encoding="utf-8") as file:
            print("=> temp_data.json: Generating new content")
            json.dump(self.data, file, ensure_ascii=False, indent=4)
