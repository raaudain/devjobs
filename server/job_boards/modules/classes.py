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


class Read_List_Of_Companies:
    def __new__(self, file_path: str):
        self.file_path = file_path
        file_path = self.file_path
        f = open(file_path, "r")
        companies = [company.strip() for company in f]
        f.close()
        random.shuffle(companies)
        return companies


class Remove_Not_Found:
    def __init__(self, file_path: str, param: str):
        self.file_path = file_path
        self.param = param
        file_path = self.file_path
        param = self.param
        f = open(file_path, "r+")
        params = [param.strip() for param in f]
        f.truncate(0)
        f.close()
        file = open(file_path, "w")
        not_found = open("./data/params/404.txt", "a")
        for p in params:
            if p != param:
                file.write(p+"\n")
            else:
                not_found.write(p+"\n")
        file.close()
        not_found.close()


class Filter_Jobs:
    def __init__(self, posting: dict):
        self.posting = posting
        posting = self.posting
        data = create_temp_json.data
        scraped = create_temp_json.scraped
        title = posting["title"]
        company = posting["company"]
        url = posting["url"]
        source_url = posting["source_url"]
        if ("Engineer" in title or "Data" in title or "IT " in title or "Tech" in title or "Support" in title or "Programmer" in title or "Developer" in title or "ML" in title or "SDET" in title or "devops" in title.lower() or "AWS" in title or "Cloud" in title or "Software" in title or "Help" in title) and ("Electrical" not in title and "HVAC" not in title and "Mechnical" not in title and "Manufactur" not in title and "Data Entry" not in title and "Nurse" not in title and "Maintenance" not in title and "Civil" not in title and "Environmental" not in title and "Hardware" not in title and "Front Desk" not in title and "Helper" not in title):
            data.append(posting)
            scraped.add(company)
            scraped.add(url)
            print(f"=> {source_url}: Added {title} for {company}")


class Update_Key_Values:
    def filter_companies():
        if isfile("./data/params/key_values.txt"):
            print("=> key_values: Deleting old parameters")
            t = open("./data/temp/temp_data.json", "r+")
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
