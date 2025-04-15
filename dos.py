import requests

s = requests.Session()
url = "https://www.brokenctf.com/report"
headers = {"X-HackMe": "true"}

for i in range(60):
    r = s.get(url, headers=headers)
    print(f"[{i+1}] {r.text}")
