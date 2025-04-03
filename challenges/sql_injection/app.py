import sqlite3
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Setup SQLite Database
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    # Create table if not exists
    cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
    
    # Insert admin user (if not exists)
    cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('admin', 'FLAG{sql_injection_success}')")
    
    conn.commit()
    conn.close()

init_db()  # Initialize database

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # ⚠️ Vulnerable Query (Prone to SQL Injection)
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        print(f"Executing Query: {query}")  # Debugging
        
        cursor.execute(query)  # 🚨 Direct execution of user input (bad practice)
        user = cursor.fetchone()
        conn.close()

        if user:
            return f"Welcome, {username}! Here is your flag: {user[1]}"
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

