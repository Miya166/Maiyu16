from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__, template_folder="templates")  # Ensure Flask looks for templates inside "templates" folder

# Function to check login credentials
def check_login(username, password):
    conn = sqlite3.connect("users.db")  # Connect to SQLite database
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()  # Fetch one matching user
    conn.close()
    return user  # Returns user data if credentials are correct, else None

# Route to render the login page
@app.route("/")
def show_login_page():
    return render_template("login.html")  # Flask renders login.html from the templates folder

# Route to handle login logic
@app.route("/login", methods=["POST"])
def login():
    data = request.json  # Get JSON data from frontend
    username = data.get("username")
    password = data.get("password")

    if check_login(username, password):
        return jsonify({"status": "success", "message": "Login successful!"})
    else:
        return jsonify({"status": "error", "message": "Invalid username or password!"})

if __name__ == "__main__":
    app.run(debug=True)  # Run Flask app in debug mode
