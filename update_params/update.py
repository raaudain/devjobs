import sys
import re
from data import ats


added = set()

def main():
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
        print(uri, l)
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
    main()

sys.exit(0)
