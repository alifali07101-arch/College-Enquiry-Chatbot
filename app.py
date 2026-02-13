# app.py - main backend
import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from dotenv import load_dotenv
from database import get_db_connection, init_db
from ai_provider import ask_ai
import json

load_dotenv()
init_db()  
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY") or "change_this_secret"

OFFICIAL_SITE = "https://rungta.ac.in"

def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return user

@app.route("/")
def index():
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))
    return render_template("index.html", user=user["name"])

# Signup
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        if not name or not email or not password:
            flash("All fields required.")
            return redirect(url_for("signup"))

        conn = get_db_connection()
        existing = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if existing:
            conn.close()
            flash("Email already registered. Please login.")
            return redirect(url_for("login"))

        conn.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
        conn.commit()
        conn.close()
        flash("Account created. Please login.")
        return redirect(url_for("login"))

    return render_template("signup.html")

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        
        print(f"👀 CHECK: Trying to Login -> Email: '{email}', Pass: '{password}'")

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        conn.close()

        if user:
            print(f"✅ FOUND:! Saved Password: '{user['password']}'")
        else:
            print("❌ NOT FOUND: user not found!")


        if user and user["password"] == password:
            session["user_id"] = user["id"]
            return redirect(url_for("index"))
        else:
            flash("Invalid credentials.")
            return redirect(url_for("login"))
    return render_template("login.html")

# Logout
@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("login"))

# Chat endpoint
@app.route("/chat", methods=["POST"])
def chat():
    user = get_current_user()
    if not user:
        return jsonify({"reply": "Please login first."}), 401

    data = request.get_json() or {}
    message = (data.get("message") or "").strip()
    if not message:
        return jsonify({"reply": "Please type something."})

    # Try to use predefined answers
    try:
        with open("chatbot_data/predefined_answers.json", "r") as f:
            predefined = json.load(f)
    except Exception:
        predefined = {}

    # keyword-based check
    lowered = message.lower()
    for key, ans in predefined.items():
        if key.lower() in lowered:
            bot_reply = ans
            break
    else:
        ai_resp = ask_ai(f"Context: You are a college enquiry assistant for Rungta International University. Answer concisely.\nUser: {message}")
        bot_reply = ai_resp if ai_resp else ("Sorry — I couldn't fetch AI response. Please check official site: " + OFFICIAL_SITE)

    # store to DB
    conn = get_db_connection()
    conn.execute("INSERT INTO chat_history (user_id, user_message, bot_reply) VALUES (?, ?, ?)",
                 (user["id"], message, bot_reply))
    conn.commit()
    conn.close()

    return jsonify({"reply": bot_reply})

# Chat history page
@app.route("/history")
def history():
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM chat_history WHERE user_id = ? ORDER BY timestamp DESC", (user["id"],)).fetchall()
    conn.close()
    return render_template("history.html", history=rows)

# Clear full chat history for current user
@app.route("/history/clear", methods=["POST"])
def clear_history():
    user = get_current_user()
    if not user:
        return jsonify({"status":"error","message":"Login required"}), 401
    conn = get_db_connection()
    conn.execute("DELETE FROM chat_history WHERE user_id = ?", (user["id"],))
    conn.commit()
    conn.close()
    return jsonify({"status":"ok"})



if __name__ == "__main__":
    app.run(debug=True)
