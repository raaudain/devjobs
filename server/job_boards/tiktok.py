import requests

session = requests.Session()

tt_tokens = session.get("https://www.tiktok.com").cookies.get_dict()


print(tt_tokens)

tt_csrf_token = tt_tokens["tt_csrf_token"]
tt_webid = tt_tokens["tt_webid"]
tt_webid_v2= tt_tokens["tt_webid_v2"]
ttwid= tt_tokens["ttwid"]




headers = {
    "Cookie":f"tt_csrf_token={tt_csrf_token}; tt_webid={tt_webid}; tt_webid_v2={tt_webid_v2}; ttwid={ttwid};",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

payload = {"portal_entrance":1}

x_token = requests.post("https://careers.tiktok.com/api/v1/csrf/token", json=payload, headers=headers).cookies.get_dict()

print(x_token)