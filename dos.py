import requests

s = requests.Session()

for i in range(60):
    r = s.get("https://www.brokenctf.com/report")
    print(f"[{i+1}] {r.text}")
