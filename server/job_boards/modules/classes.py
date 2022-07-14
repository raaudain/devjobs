import json
import re
import requests
import random
from os.path import isfile
from bs4 import BeautifulSoup


class Read_List_Of_Companies:
    def __new__(self, file_path: str):
        self.file_path = file_path
        file_path = self.file_path
        with open(file_path, "r") as f:
            companies = [company.strip() for company in f]
            random.shuffle(companies)
            return companies


class Remove_Not_Found:
    def __init__(self, file_path: str, param: str):
        self.file_path = file_path
        self.param = param
        file_path = self.file_path
        param = self.param
        with open(file_path, "r+") as f, open(file_path, "w") as file:
            params = [param.strip() for param in f]
            f.truncate(0)
            for p in params:
                if p != param:
                    file.write(p+"\n")


class Get_Stored_Data:
    def __new__(self, file_path: str):
        self.file_path = file_path
        file_path = self.file_path
        table = {}
        with open(file_path, "r") as f:
            for e in f:
                e = e.split("`")
                p = e[0]
                name = e[1]
                img = e[2]
                table[p] = {
                    "name": name if name else p.capitalize(),
                    "logo": img.rstrip("\n") if len(img) > 6 else None
                }
        return table


class Filter_Jobs:
    def __init__(self, posting: dict):
        self.posting = posting
        posting = self.posting

        data = Create_JSON.data
        scraped = Create_JSON.scraped
        title = posting["title"]
        company = posting["company"]
        url = posting["url"]
        wanted = ["Engineer", "Data", "IT ",  "Tech ", "QA", "Programmer", "Developer", "ML", "SDET", "DevOps", "AWS", "Cloud", "Software", "Help", "Web ", "Front End", "Agile", "Cyber"]
        wanted = "(%s)" % "|".join(wanted)
        unwanted = ["Elect", "HVAC", "Mechanical", "Manufactur", "Data Entry", "Nurse", "Maintenance", "Civil", "Environmental", "Hardware", "Front Desk", "Helper", "Peer Support", "Bridge", "Water", "Dispatch", "Saw", "Facilities", "AML", "Sheet Metal", "Metallurgical", "Materials", "Expeditor", "Job Developer"]
        unwanted = "(%s)" % "|".join(unwanted)

        if re.search(wanted, title) is not None and re.search(unwanted, title) is None:
            data.append(posting)
            scraped.add(company)
            scraped.add(url)


class Update_Key_Values:
    def filter_companies():
        url = "https://www.keyvalues.com/"
        html = requests.get(url).text
        soup = BeautifulSoup(html, "lxml")
        with open("./data/params/key_values.txt", "w+") as company, open("./data/params/key_values_unwanted.txt", "r") as f:
            links = soup.find_all("a", class_="thumbnail-link", href=True)
            unwanted = [w.strip() for w in f]
            for link in links:
                if link["href"] not in unwanted:
                    company.write(link["href"]+"\n")
            print("=> key_values: Updated parameters")


class Create_JSON:
    data = []
    scraped = set()

    def create_temp_file(item):
        temp = "./data/temp/temp_data.json"
        with open(temp, "w+", encoding="utf-8") as file:
            print("=> temp_data.json: Generating new data")
            json.dump(item, file, ensure_ascii=False, indent=4)

    def create_file():
        temp = "./data/temp/temp_data.json"
        main = "./data/data.json"
        with open(main, "w+", encoding="utf-8") as file, open(temp, "r+") as f:
            data = json.load(f)
            ordered_data = sorted(
                data, key=lambda i: i["timestamp"], reverse=True)
            print("=> data.json: Generating new data")
            json.dump(ordered_data, file, ensure_ascii=False, indent=4)
            if isfile(temp):
                print("=> temp_data.json: Deleting temporary data")
                f.truncate(0)
