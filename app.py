from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# ✅ IMPORTANT FOR SUBMISSION:
# Before you submit, remove your real password (teacher request).
# You can leave password as "" if your local MySQL has no password,
# OR replace it with a placeholder like "YOUR_PASSWORD_HERE" (but not your real one).
DB_CONFIG = {
     "host": "localhost",
 "user": "root",
"password": "", # <-- remove/blank before submitting
"database": "project_db"
}

def get_connection():
 return mysql.connector.connect(**DB_CONFIG)

@app.route("/")
def home():
   return render_template("home.html")

@app.route("/form")
def form():
 return render_template("form.html")

@app.route("/submit", methods=["POST"])
def submit():
    # 10 required fields
    full_name = request.form["full_name"]
    email = request.form["email"]
    phone = request.form["phone"]
    age = request.form["age"]
    city = request.form["city"]
    country = request.form["country"]
    favorite_language = request.form["favorite_language"]
    experience_level = request.form["experience_level"]
    newsletter = request.form["newsletter"]
    comments = request.form["comments"]

    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    INSERT INTO survey
    (full_name, email, phone, age, city, country, favorite_language, experience_level, newsletter, comments) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        full_name, email, phone, age, city, country,
        favorite_language, experience_level, newsletter, comments
    )
    cursor.execute(sql, values)
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("display"))

@app.route("/display")
def display():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM survey ORDER BY created_at DESC")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("display.html", rows=rows)

if __name__ == "__main__":
  app.run(debug=True)
