import re


def process_urls(urls, params, uri):
    links = [url.strip() for url in urls]

    with open(params, "r") as p:
        text = [company.lower().strip() for company in p]


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
    added = set()

    try:
        for c in words_list:
            c = c.split("?")[0]
            d = c.lower()

            if d not in text and d not in added and d != "j":
                with open(params, "a") as a:
                    a.write(f"{c}\n")
                added.add(d)
    except Exception as e:
        print(f"{params}: Error: {e}.")
