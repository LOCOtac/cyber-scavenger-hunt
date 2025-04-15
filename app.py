from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("storefront.html")

@app.route("/product/<int:product_id>")
def product(product_id):
    # Dummy product data
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

@app.route("/robots.txt")
def robots():
    return "Disallow: /admin\nDisallow: /hidden-flag"

@app.route("/admin")
def admin():
    return "🎉 You found the secret admin panel! FLAG-ADMIN999"

@app.route("/hidden-flag")
def hidden_flag():
    return "You found a hidden endpoint. FLAG-HIDDEN777"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
