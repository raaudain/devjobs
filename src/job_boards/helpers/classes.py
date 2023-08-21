import json
import re
import requests
import random
from os.path import isfile
from bs4 import BeautifulSoup


class ProcessCompanyJobData:
    def read_list_of_companies(self, file_path: str):
        with open(file_path, "r") as f:
            companies = [company.strip() for company in f]
            random.shuffle(companies)
            return companies

    def remove_not_found(self, file_path: str, param: str):
        f = open(file_path, "r+")
        params = [param.strip() for param in f]
        f.truncate(0)
        f.close()

        file = open(file_path, "w")
        not_found = open("src/data/params/404.txt", "a")

        for p in params:
            if p != param:
                file.write(p+"\n")
            else:
                not_found.write(p+"\n")

        file.close()
        not_found.close()

    def get_stored_data(self, file_path: str):
        table = {}

        with open(file_path, "r") as f:
            for item in f:
                item = item.split("`")
                p = item[0]
                name = item[1]
                img = item[2]
                table[p] = {
                    "name": name if name else p.capitalize(),
                    "logo": img.rstrip("\n") if len(img) > 6 else None
                }
        return table

    def filter_jobs(self, posting: dict):
        data = CreateJson().data
        scraped = CreateJson().scraped

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

    def filter_key_values_companies(self):
        url = "https://www.keyvalues.com/"
        html = requests.get(url).text
        soup = BeautifulSoup(html, "lxml")

        with open("src/data/params/key_values.txt", "w+") as company, open("src/data/params/key_values_unwanted.txt", "r") as f:
            links = soup.find_all("a", class_="thumbnail-link", href=True)
            unwanted = [w.strip() for w in f]

            for link in links:
                if link["href"] not in unwanted:
                    company.write(link["href"]+"\n")
            print("=> key_values: Updated parameters")

class CreateJson:
    data = []
    scraped = set()

    def create_temp_file(self):
        temp = "src/data/temp/temp_data.json"
        with open(temp, "w+", encoding="utf-8") as file:
            print("=> temp_data.json: Generating new data")
            json.dump(self.data, file, ensure_ascii=False, indent=4)

    def create_file(self):
        temp = "src/data/temp/temp_data.json"
        main = "src/data/data.json"

        with open(main, "w+", encoding="utf-8") as file, open(temp, "r+") as f:
            data = json.load(f)
            ordered_data = sorted(
                data, key=lambda i: i["timestamp"], reverse=True)
            print("=> data.json: Generating new data")
            json.dump(ordered_data, file, ensure_ascii=False, indent=4)

            if isfile(temp):
                print("=> temp_data.json: Deleting temporary data")
                f.truncate(0)
