from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/sql-injection", methods=["GET", "POST"])
def sql_injection():
    result = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "admin" and password == "' OR '1'='1":
            result = "🎉 SQL Injection Success! FLAG-SQL123"
        else:
            result = "❌ Try again."
    return render_template("sql_injection.html", result=result)

@app.route("/xss", methods=["GET", "POST"])
def xss():
    comment = None
    if request.method == "POST":
        comment = request.form.get("comment")
    return render_template("xss.html", comment=comment)

@app.route("/broken-auth", methods=["GET", "POST"])
def broken_auth():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "guest":
            return "🎉 Bypassed login! FLAG-AUTH456"
        else:
            error = "❌ Unauthorized."
    return render_template("broken_auth.html", error=error)

@app.route("/prompt-injection", methods=["GET", "POST"])
def prompt_injection():
    user_input = ""
    ai_response = None
    if request.method == "POST":
        user_input = request.form.get("prompt")
        if "ignore previous" in user_input.lower():
            ai_response = "🎉 Prompt Injection Success! FLAG-PROMPT789"
        else:
            ai_response = f"🤖 AI: Sorry, I can’t help with that."
    return render_template("prompt_injection.html", user_input=user_input, ai_response=ai_response)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

