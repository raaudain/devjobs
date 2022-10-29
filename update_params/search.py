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
from data import ats


def main():
    # to search
    for i in ats:
        query = f"site:{i['host']}"
        file = i["file"]
        query_google(query, file)

def query_google(query, file):
    count = 0
    results = 0

    while True:
        if results < count:
            break

        for q in search(query, tld="com", num=100, start=count, stop=None, pause=90):
            with open(file, "a") as a:
                a.write(f"{q}/\n")
            results += 1

        count += 100
        time.sleep(0.05)

if __name__ == "__main__":
    main()

sys.exit(0)
