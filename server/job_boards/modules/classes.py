import json
import requests
import random
from os.path import isfile
from bs4 import BeautifulSoup


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
        data = Create_JSON.data
        scraped = Create_JSON.scraped
        title = posting["title"]
        company = posting["company"]
        url = posting["url"]
        source_url = posting["source_url"]
        if ("Engineer" in title or "Data" in title or "IT " in title or "Tech " in title or "QA" in title or "Programmer" in title or "Developer" in title or "ML" in title or "SDET" in title or "devops" in title.lower() or "AWS" in title or "Cloud" in title or "Software" in title or "Help" in title or "Web" in title or "Front End" in title or "Agile" in title and "Cyber" in title) and ("Elect" not in title and "HVAC" not in title and "Mechanical" not in title and "Manufactur" not in title and "Data Entry" not in title and "Nurse" not in title and "Maintenance" not in title and "Civil" not in title and "Environmental" not in title and "Hardware" not in title and "Front Desk" not in title and "Helper" not in title and "Peer Support" not in title and "Bridge" not in title and "Water" not in title and "Dispatch" not in title and "Saw" not in title and "Facilities" not in title and "AML" not in title and "Sheet Metal" not in title and "Metallurgical" not in title and "Materials" not in title):
            data.append(posting)
            scraped.add(company)
            scraped.add(url)


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
        links = soup.find_all("a", class_="thumbnail-link", href=True)
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

    def create_temp_file(item):
        temp = "./data/temp/temp_data.json"
        if isfile(temp):
            print("=> temp_data.json: Deleting old data")
            t = open(temp, "r+")
            t.truncate(0)
            t.close()
        with open(temp, "a", encoding="utf-8") as file:
            print("=> temp_data.json: Generating new data")
            json.dump(item, file, ensure_ascii=False, indent=4)

    def create_file():
        temp = "./data/temp/temp_data.json"
        f = open(temp, "r")
        data = json.load(f)
        f.close()
        main = "./data/data.json"
        if isfile(main):
            print("=> data.json: Deleting old data")
            m = open(main, "r+")
            m.truncate(0)
            m.close()
        ordered_data = sorted(data, key=lambda i: i["timestamp"], reverse=True)
        with open(main, "a", encoding="utf-8") as file:
            print("=> data.json: Generating new data")
            json.dump(ordered_data, file, ensure_ascii=False, indent=4)
        if isfile(temp):
            print("=> temp_data.json: Deleting temporary data")
            t = open(temp, "r+")
            t.truncate(0)
            t.close()
