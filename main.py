# main.py
from flask import Flask, jsonify, request, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # For session management

# Create temporary database
conn = sqlite3.connect(':memory:', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE users (username TEXT, password TEXT)''')
cursor.execute("INSERT INTO users VALUES ('user1', 'pass1')")
cursor.execute("INSERT INTO users VALUES ('user2', 'pass2')")
conn.commit()

@app.route("/")
def root():
    """
    Root endpoint to check API health.
    """
    return jsonify({"status": "ok", "version": "1.0.0"})

@app.route("/add/<int:a>/<int:b>")
def add(a, b):
    """
    Simple logic function to test mathematics.
    """
    return jsonify({"result": a + b})

@app.route('/login', methods=['POST'])
def login():
    """
    Login function with temporary database.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    if cursor.fetchone():
        session['logged_in'] = True
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@app.route("/subtract/<int:a>/<int:b>")
def subtract(a, b):
    """
    Subtract function that can only be accessed after login.
    """
    if 'logged_in' not in session:
        return jsonify({"message": "Login required"}), 401
    return jsonify({"result": a - b})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)