import sys
import re


ats = [
    {
        "file": "./temp/workable_temp.txt",
        "params": "../server/data/params/workable.txt",
        "uri": r"https://apply.workable.com/(.*?)/"
    },
    {
        "file": "./temp/greenhouse_temp.txt",
        "params": "../server/data/params/greenhouse_io.txt",
        "uri": r"https://boards.greenhouse.io/(.*?)/"
    },
    {
        "file": "./temp/lever_temp.txt",
        "params": "../server/data/params/lever_co.txt",
        "uri": r"https://jobs.lever.co/(.*?)/"
    },
    {
        "file": "./temp/smartrecruiters_temp.txt",
        "params": "../server/data/params/smartrecruiters.txt",
        "uri": r"https://careers.smartrecruiters.com/(.*?)/"
    },
    {
        "file": "./temp/ashbyhq_temp.txt",
        "params": "../server/data/params/ashbyhq.txt",
        "uri": r"https://jobs.ashbyhq.com/(.*?)/"
    },
    {
        "file": "./temp/jazzhr_temp.txt",
        "params": "../server/data/params/jazzhr.txt",
        "uri": r"https://(.*?).applytojob.com/"
    },
    {
        "file": "./temp/breezyhr_temp.txt",
        "params": "../server/data/params/breezyhr.txt",
        "uri": r"https://(.*?).breezy.hr/"
    },
    {
        "file": "./temp/jobvite_temp.txt",
        "params": "../server/data/params/jobvite.txt",
        "uri": r"https://jobs.jobvite.com/(.*?)/"
    },
    {
        "file": "./temp/recruiterbox_temp.txt",
        "params": "../server/data/params/recruiterbox.txt",
        "uri": r"https://(.*?).recruiterbox.com/jobs"
    },
    {
        "file": "./temp/bamboohr_temp.txt",
        "params": "../server/data/params/bamboohr.txt",
        "uri": r"https://(.*?).bamboohr.com/jobs"
    },
    {
        "file": "./temp/comeet_temp.txt",
        "params": "../server/data/params/comeet.txt",
        "uri": r"https://www.comeet.com/jobs/(.*?)/"
    },
    {
        "file": "./temp/eightfold_temp.txt",
        "params": "../server/data/params/eightfold.txt",
        "uri": r"https://(.*?).eightfold.ai/careers/"
    },
    {
        "file": "./temp/clearcompany_temp.txt",
        "params": "../server/data/params/clearcompany.txt",
        "uri": r"http://(.*?).hrmdirect.com/"
    },
    {
        "file": "./temp/polymer_temp.txt",
        "params": "../server/data/params/polymer.txt",
        "uri": r"https://jobs.polymer.co/(.*?)/"
    },
    {
        "file": "./temp/recruitee_temp.txt",
        "params": "../server/data/params/recruitee.txt",
        "uri": r"https://(.*?).recruitee.com/"
    },
]

added = set()

def start():
  for i in ats:
    params = i["params"]
    uri = i["uri"]
    with open(params, "r") as p:
        text = [company.lower().strip() for company in p]
    with open(i["file"], "r") as f:
        links = [x.strip() for x in f]
    words_list = filter_list(links, uri)
    update_params(words_list, params, text)

def filter_list(links, uri):
    w = []
    for l in links:
        word = re.findall(uri, l)
        if word:
            w.append(*word)
    return w

def update_params(words_list, params, text):
    for c in words_list:
        d = c.lower()
        if d not in text and d not in added and d != "j":
            with open(params, "a") as a:
                a.write(f"{c}\n")
            added.add(d)

if __name__ == "__main__":
  start()

sys.exit(0)
