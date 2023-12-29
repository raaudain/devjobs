#!/user/bin/env python3

import sys
sys.path.insert(0, ".")
from src.update_params.utils import ats
from src.update_params.tools import query_google, process_urls


def main():
    for a in ats:
        query = f"site:{a['host']}"
        print("\ncurrent query:", query)
        params = a["params"]
        uri = a["uri"]
        urls = query_google(query)
        process_urls(urls, params, uri)

if __name__ == "__main__":
    main()

