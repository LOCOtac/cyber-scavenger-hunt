from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = "cyberhunt-secret"  # for session tracking

VALID_FLAGS = {
    "FLAG-SQL123": 10,
    "FLAG-XSS456": 10,
    "FLAG-UPLOAD321": 15,
    "FLAG-ADMIN999": 20,
    "FLAG-HIDDEN777": 15,
    "FLAG-JS666": 10,
    "FLAG-CHAT999": 20
}

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

@app.route("/robots.txt")
def robots():
    return "Disallow: /admin\nDisallow: /hidden-flag"

@app.route("/admin")
def admin():
    return "🎉 You found the secret admin panel! FLAG-ADMIN999"

@app.route("/hidden-flag")
def hidden_flag():
    return "You found a hidden endpoint. FLAG-HIDDEN777"

@app.route("/submit", methods=["GET", "POST"])
def submit():
    message = None
    score = session.get("score", 0)
    solved_flags = session.get("solved", [])

    if request.method == "POST":
        flag = request.form.get("flag").strip()
        if flag in VALID_FLAGS and flag not in solved_flags:
            score += VALID_FLAGS[flag]
            solved_flags.append(flag)
            session["score"] = score
            session["solved"] = solved_flags
            message = f"✅ Correct! You earned {VALID_FLAGS[flag]} points."
        elif flag in solved_flags:
            message = "⚠️ You've already submitted this flag."
        else:
            message = "❌ Invalid flag."

    return render_template("submit.html", message=message, score=score, solved=solved_flags)

@app.route("/scoreboard")
def scoreboard():
    score = session.get("score", 0)
    solved = session.get("solved", [])
    return render_template("scoreboard.html", score=score, solved=solved)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
