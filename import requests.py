import requests

# Replace with your domain
BASE_URL = "http://localhost:5000"  # or your deployed URL like https://brokenctf.com

# List of challenge routes
ROUTES = [
    "/", "/review", "/upload", "/chat", "/redirect?next=https://example.com",
    "/order?id=2", "/report", "/cookies", "/debug-leak", "/jwt-challenge",
    "/robots.txt", "/admin", "/hidden-flag", "/submit", "/scoreboard", "/leaderboard",
    "/api/products", "/user-agent-check", "/ai-helper", "/register", "/profile",
    "/stats", "/race-checkout", "/reset?token=admin-reset-token", "/vault/items",
    "/admin/dashboard?secret=hunter2", "/ai-inception", "/chat-ai-bot", "/ai/encrypted-payload",
    "/graphql-search", "/product/review-bombed", "/admin-login", "/limited-access",
    "/api/user?id=124", "/super-admin-portal-9283", "/health", "/logs",
    "/ai-log-login", "/ai-log", "/cart", "/cart/clear"
]

print("🔍 Checking CTF Routes...\n")

for route in ROUTES:
    try:
        full_url = f"{BASE_URL}{route}"
        r = requests.get(full_url, timeout=5)
        status = r.status_code
        if status == 200:
            print(f"[✅] {route} → 200 OK")
        elif status == 302:
            print(f"[↪️] {route} → Redirected")
        elif status == 403:
            print(f"[🔒] {route} → 403 Forbidden")
        elif status == 404:
            print(f"[❌] {route} → 404 Not Found")
        else:
            print(f"[⚠️] {route} → {status}")
    except requests.exceptions.RequestException as e:
        print(f"[❗] {route} → Error: {str(e)}")

print("\n✅ Route check complete.")
