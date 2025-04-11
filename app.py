from flask import Flask, render_template, request

import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "default-secret-key")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/challenge/<int:id>")
def challenge(id):
    return render_template("challenge.html", challenge_id=id)

@app.route("/submit", methods=["POST"])
def submit():
    answer = request.form.get("answer", "")
    if answer == "flag{correct_flag}":
        return render_template("success.html")
    return render_template("fail.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
