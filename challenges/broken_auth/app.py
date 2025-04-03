from flask import Flask, request, redirect, make_response, render_template_string

app = Flask(__name__)

# Simulated user database
users = {
    "admin": "password123",
    "user": "userpass"
}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Check credentials (no password hashing, bad practice)
        if username in users and users[username] == password:
            response = make_response(redirect("/dashboard"))
            response.set_cookie("session_id", username)  # 🚨 Weak session token! (Fixed to match browser)
            return response
        else:
            return "Invalid credentials"

    return render_template_string("""
        <h2>Login</h2>
        <form method="post">
            <input type="text" name="username" placeholder="Username"><br>
            <input type="password" name="password" placeholder="Password"><br>
            <button type="submit">Login</button>
        </form>
    """)

@app.route("/dashboard")
def dashboard():
    session = request.cookies.get("session_id")  # Fixed: Now matches the browser cookie

    # Allow access to any valid session value (Vulnerable to session hijacking)
    if session:
        return f"Welcome, {session}! Your session token is weak. Try changing it!"
    else:
        return "Unauthorized. Please log in."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
