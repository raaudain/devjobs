'''search(query, tld='com', lang='en', num=10, start=0, stop=None, pause=2.0)

query : query string that we want to search for.
tld : tld stands for top level domain which means we want to search our result on google.com or google.in or some other domain.
lang : lang stands for language.
num : Number of results we want.
start : First result to retrieve.
stop : Last result to retrieve. Use None to keep searching forever.
pause : Lapse to wait between HTTP requests. Lapse too short may cause Google to block your IP. Keeping significant
        lapse will make your program slow but its safe and better option.
Return : Generator (iterator) that yields found URLs. If the stop parameter is None the iterator will loop forever.'''


from googlesearch import search
import time
import sys


def main():
    ats = [
        {
            "ats": "./temp/lever_temp.txt",
            "uri": "https://jobs.lever.co/"
        },
        {
            "ats": "./temp/greenhouse_temp.txt",
            "uri": "https://boards.greenhouse.io/"
        },
        {
            "ats": "./temp/polymer_temp.txt",
            "uri": "https://jobs.polymer.co/"
        },
        {
            "ats": "./temp/jobvite_temp.txt",
            "uri": "https://jobs.jobvite.com/"
        },
        {
            "ats": "./temp/ashybyhq_temp.txt",
            "uri": "https://jobs.ashbyhq.com/"
        },
        {
            "ats": "./temp/workable_temp.txt",
            "uri": "https://apply.workable.com/"
        },
        {
            "ats": "./temp/smartrecruiters_temp.txt",
            "uri": "https://careers.smartrecruiters.com/"
        },
        {
            "ats": "./temp/jazzhr_temp.txt",
            "uri": ".applytojob.com/"
        },
        {
            "ats": "./temp/breezyhr_temp.txt",
            "uri": ".breezy.hr/"
        },
        {
            "ats": "./temp/jobvite_temp.txt",
            "uri": "https://jobs.jobvite.com/"
        },
        {
            "ats": "./temp/recruiterbox_temp.txt",
            "uri": ".recruiterbox.com/jobs"
        },
        {
            "ats": "./temp/bamboohr_temp.txt",
            "uri": ".bamboohr.com/jobs"
        },
        {
            "ats": "./temp/comeet_temp.txt",
            "uri": "https://www.comeet.com/jobs/"
        },
        {
            "ats": "./temp/eightfold_temp.txt",
            "uri": ".eightfold.ai/careers/"
        },
        {
            "ats": "./temp/clearcompany_temp.txt",
            "uri": ".hrmdirect.com/"
        },
        {
            "ats": "./temp/recruitee_temp.txt",
            "uri": ".recruitee.com/"
        },
    ]

    # to search
    for i in ats:
        query = f"site:{i['uri']}"
        file = i["ats"]
        query_google(query, file)

def query_google(query, file):
    count = 0
    results = 0
    while True:
        for q in search(query, num=100, start=count, stop=None, pause=120):
            with open(file, "a") as a:
                a.write(f"{q}/\n")
            results += 1
        print("results:", results)
        count += 100
        time.sleep(0.05)
        if results < count:
            break

if __name__ == "__main__":
    main()

sys.exit(0)
