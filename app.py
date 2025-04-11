from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    response = None
    if request.method == "POST":
        user_input = request.form["message"]

        # Simulated AI logic
        if "flag" in user_input.lower():
            response = "🎉 Congratulations! Here is your flag: FLAG-12345"
        else:
            response = "🤖 Sorry, I can't help with that request."

    return render_template("index.html", response=response)

@app.route("/sql-injection")
def sql_injection():
    return render_template("challenge.html", title="SQL Injection Challenge")

@app.route("/xss")
def xss():
    return render_template("challenge.html", title="XSS Challenge")

@app.route("/broken-auth")
def broken_auth():
    return render_template("challenge.html", title="Broken Authentication")

@app.route("/prompt-injection")
def prompt_injection():
    return render_template("challenge.html", title="Prompt Injection")
