import sys
from data import ats
from search_for_domains import query_google
from update_ats_params import process_urls


def main():
    for a in ats:
        query = f"site:{a['host']}"
        print("current query:", query)
        params = a["params"]
        uri = a["uri"]
        urls = query_google(query)
        process_urls(urls, params, uri)

if __name__ == "__main__":
    main()
    sys.exit(0)
