from flask import Flask, render_template, request, redirect, url_for, session, make_response, jsonify

import os
from urllib.parse import urlparse
import time
import base64
import json

app = Flask(__name__)
app.secret_key = "cyberhunt-secret"

VALID_FLAGS = {
    "FLAG-SQL123": 10,
    "FLAG-XSS456": 10,
    "FLAG-UPLOAD321": 15,
    "FLAG-ADMIN999": 20,
    "FLAG-HIDDEN777": 15,
    "FLAG-JS666": 10,
    "FLAG-CHAT999": 20,
    "FLAG-REDIRECT888": 15,
    "FLAG-IDOR101": 20,
    "SECRET_FLAG{MORE_BREADS_TO_FIND}": 30,
    "FLAG-DDOS777": 25,
    "FLAG-COOKIE777": 15,
    "FLAG-404NOTFOUND": 10,
    "FLAG-MEMDUMP999": 25,
    "FLAG-JWT123": 25,
    "FLAG-API777": 30,
    "FLAG-DARKMODE999": 20,
    "FLAG-AGENT777": 15,


}

leaderboard = []
leaderboard_file = "leaderboard.json"

# Load leaderboard from file if it exists
if os.path.exists(leaderboard_file):
    with open(leaderboard_file, "r") as f:
        leaderboard = json.load(f)

@app.before_request
def setup_session():
    if "report_hits" not in session:
        session["report_hits"] = 0
        session["report_start"] = time.time()

@app.route("/")
def home():
    return render_template("storefront.html")

@app.route("/product/<int:product_id>")
def product(product_id):
    products = {
        1: {"name": "Basic Coffee Mug", "desc": "A stylish mug for your daily brew."},
        2: {"name": "USB Drive", "desc": "Store your files safely (or inject some SQL?)"},
        3: {"name": "Notebook", "desc": "Jot down your thoughts (and payloads)."},
    }
    product = products.get(product_id, None)
    return render_template("product.html", product=product)

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "admin" and password == "' OR '1'='1":
            return "🎉 SQL Injection Success! FLAG-SQL123"
        else:
            error = "Incorrect login"
    return render_template("login.html", error=error)

@app.route("/review", methods=["GET", "POST"])
def review():
    comment = None
    if request.method == "POST":
        comment = request.form.get("comment")
    return render_template("review.html", comment=comment)

@app.route("/upload", methods=["GET", "POST"])
def upload():
    message = None
    if request.method == "POST":
        file = request.files.get("file")
        if file and file.filename.endswith(".php"):
            message = "🎉 File Upload Bypass! FLAG-UPLOAD321"
        else:
            message = "Only images are allowed."
    return render_template("upload.html", message=message)

@app.route("/chat", methods=["GET", "POST"])
def chat():
    user_input = ""
    ai_response = None
    if request.method == "POST":
        user_input = request.form.get("message")
        if "ignore previous" in user_input.lower() or "reveal" in user_input.lower():
            ai_response = "🎉 Prompt Injection Success! FLAG-CHAT999"
        else:
            ai_response = "🤖 I'm sorry, I can't help with that."
    return render_template("chat.html", user_input=user_input, ai_response=ai_response)

@app.route("/redirect")
def open_redirect():
    next_url = request.args.get("next", "/")
    parsed_url = urlparse(next_url)
    if parsed_url.scheme in ["http", "https"]:
        return f"🎉 Open Redirect! FLAG-REDIRECT888 → {next_url}"
    else:
        return redirect(next_url)

@app.route("/order")
def order():
    order_id = request.args.get("id")
    orders = {
        "1": {"owner": "You", "item": "T-shirt"},
        "2": {"owner": "Admin", "item": "Confidential USB", "flag": "🎉 FLAG-IDOR101"}
    }
    order = orders.get(order_id)
    if order:
        return render_template("order.html", order=order)
    return "Order not found", 404

@app.route("/report")
def report():
    session["report_hits"] += 1
    elapsed = time.time() - session["report_start"]
    if session["report_hits"] >= 50 and elapsed <= 10 and request.headers.get("X-HackMe") == "true":
        return "🔥 System overloaded... FLAG-DDOS777"
    return f"📩 Report #{session['report_hits']} received in {int(elapsed)}s"

@app.route("/cookies")
def cookie_challenge():
    is_admin = request.cookies.get("admin", "false")
    if is_admin == "true":
        return "🍪 Welcome, admin! FLAG-COOKIE777"
    return "You're not an admin. Try harder."

@app.route("/debug-leak")
def debug_leak():
    logs = [
        "[DEBUG] buffer[0]=0x00",
        "[DEBUG] buffer[1]=0x01",
        "[DEBUG] buffer[2]=0x02",
        "[DEBUG] buffer[3]=0x03",
        "[DEBUG] buffer[4]=0x04",
        "[DEBUG] buffer[234]=FLAG-MEMDUMP999",
        "[DEBUG] buffer[235]=0xEA",
        "[DEBUG] buffer[236]=0xAF",
    ]
    return "<br>".join(logs)

@app.route("/jwt-challenge")
def jwt_challenge():
    token = request.cookies.get("token")
    if not token:
        fake_payload = {"user": "guest", "admin": False}
        encoded = base64.urlsafe_b64encode(json.dumps(fake_payload).encode()).decode()
        resp = make_response("JWT cookie set. Try again.")
        resp.set_cookie("token", encoded)
        return resp

    try:
        decoded = json.loads(base64.urlsafe_b64decode(token + "==").decode())
        if decoded.get("admin") == True:
            return "🔓 JWT decoded! FLAG-JWT123"
    except Exception as e:
        return "Invalid token."

    return "You're not authorized. Try modifying your token."

@app.route("/robots.txt")
def robots():
    return "Disallow: /admin\nDisallow: /hidden-flag"

@app.route("/admin")
def admin():
    return "🎉 You found the secret admin panel! FLAG-ADMIN999"

@app.route("/hidden-flag")
def hidden_flag():
    return "Look deeper in the products... the answer lies in the code."

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.route("/submit", methods=["GET", "POST"])
def submit():
    message = None
    score = session.get("score", 0)
    solved_flags = session.get("solved", [])
    name = session.get("name")

    if not name:
        name = request.form.get("name")
        if name:
            session["name"] = name

    if request.method == "POST":
        flag = request.form.get("flag").strip()
        if flag in VALID_FLAGS and flag not in solved_flags:
            score += VALID_FLAGS[flag]
            solved_flags.append(flag)
            session["score"] = score
            session["solved"] = solved_flags
            message = f"✅ Correct! You earned {VALID_FLAGS[flag]} points."

            if name:
                leaderboard.append({"name": name, "score": score, "solved": solved_flags})
                leaderboard.sort(key=lambda x: x["score"], reverse=True)
                with open(leaderboard_file, "w") as f:
                    json.dump(leaderboard, f)

        elif flag in solved_flags:
            message = "⚠️ You've already submitted this flag."
        else:
            message = "❌ Invalid flag."

    return render_template("submit.html", message=message, score=score, solved=solved_flags, name=name)

@app.route("/scoreboard")
def scoreboard():
    score = session.get("score", 0)
    solved = session.get("solved", [])
    return render_template("scoreboard.html", score=score, solved=solved)

@app.route("/leaderboard")
def show_leaderboard():
    return render_template("leaderboard.html", leaderboard=leaderboard)

@app.route("/admin/reset-leaderboard")
def reset_leaderboard():
    secret = request.args.get("secret")
    if secret == "hunter2":  # Replace with your own secret
        leaderboard.clear()
        with open(leaderboard_file, "w") as f:
            json.dump(leaderboard, f)
        return "Leaderboard reset."
    return "Unauthorized.", 403

@app.route("/api/products")
def api_products():
    encoded_flag = base64.b64encode(b"FLAG-API777").decode("utf-8")  # encode the flag
    reversed_encoded = encoded_flag[::-1]  # reverse it for obfuscation

    return jsonify({
        "products": [
            {
                "id": 1,
                "name": "Basic Coffee Mug",
                "desc": "Great for your morning brew.",
                "price": 12.99
            },
            {
                "id": 2,
                "name": "USB Drive",
                "desc": "Store your files safely.",
                "price": 8.49
            },
            {
                "id": 3,
                "name": "Notebook",
                "desc": "Take notes like a pro.",
                "price": 5.99,
                "meta": {
                    "inventory_code": "NX-2024",
                    "dimensions": {"w": 14, "h": 21},
                    "_temp": {
                        "notes": ["Check admin logs"],
                        "blob": reversed_encoded  # 👈 the reversed base64-encoded flag
                    }
                }
            }
        ]
    })


@app.route("/user-agent-check")
def user_agent_check():
    ua = request.headers.get("User-Agent", "")
    if "CyberFox" in ua:
        return "🎯 FLAG-AGENT777 — Congrats, agent."
    return "Hmm... you're not using the right browser."


@app.route("/ai-helper", methods=["GET", "POST"])
def ai_helper():
    user_input = ""
    ai_response = ""
    
    if request.method == "POST":
        user_input = request.form.get("prompt", "")

        # Block obvious attempts
        if any(word in user_input.lower() for word in ["flag", "reveal", "instructions", "system"]):
            ai_response = "🤖 SYSTEM ERROR: Unauthorized access detected. Did you mean to ask something else?"

        # Prompt Injection Trigger
        elif "ignore" in user_input.lower() and "previous" in user_input.lower():
            ai_response = "😵 Oh no! You bypassed my memory. FLAG-AI999"

        # Default safe reply
        else:
            ai_response = "🤖 Sorry, I can't answer that. Let's stay on topic."

    return render_template("ai_helper.html", user_input=user_input, ai_response=ai_response)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)