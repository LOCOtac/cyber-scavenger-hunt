from flask import Flask, request, render_template_string

app = Flask(__name__)

# Store comments (resets when container restarts)
comments = []

@app.route("/", methods=["GET", "POST"])
def xss_challenge():
    if request.method == "POST":
        comment = request.form.get("comment")

        if comment.strip():  # Prevent empty input
            comments.append(comment)  # 🚨 No sanitization (XSS Vulnerability)

    # Display all comments (including potential XSS payloads)
    page = """
    <h2>Leave a Comment</h2>
    <form method="post">
        <textarea name="comment" placeholder="Enter your comment here..."></textarea><br>
        <button type="submit">Submit</button>
    </form>
    <h3>Comments:</h3>
    <ul>
    """ + "".join(f"<li>{c}</li>" for c in comments) + "</ul>"

    return render_template_string(page)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

