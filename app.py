import os
import sqlite3
from flask import Flask, jsonify, render_template, request, session

app = Flask(__name__)
app.secret_key = "harshit_super_secret_admin_key"

DB_FILE = "survey.db"


def init_db():
  conn = sqlite3.connect(DB_FILE)
  cursor = conn.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            gmail TEXT,
            language TEXT,
            q1_education TEXT,
            q2_status TEXT,
            q3_field TEXT,
            q4_challenge TEXT,
            q5_sufficiency TEXT,
            q6_gap TEXT,
            q7_confidence TEXT,
            q8_importance TEXT,
            q9_format TEXT,
            q10_time TEXT,
            q11_duration TEXT,
            q12_investment TEXT,
            q13_payment TEXT,
            q14_priority TEXT,
            q15_interest TEXT,
            q16_problem TEXT
        )
    """)
  conn.commit()
  conn.close()


@app.route("/")
def index():
  return render_template("index.html")


@app.route("/admin")
def admin_portal():
  if not session.get("logged_in"):
    return render_template("admin_login.html")
  return render_template("admin.html")


@app.route("/admin_login", methods=["POST"])
def admin_login():
  data = request.json
  password = data.get("password")
  if password == "jhakaas":
    session["logged_in"] = True
    return jsonify({"status": "success"})
  return jsonify({"status": "error", "message": "Wrong password!"}), 401


@app.route("/logout")
def logout():
  session.pop("logged_in", None)
  return jsonify({"status": "success"})


@app.route("/get_data")
def get_data():
  if not session.get("logged_in"):
    return jsonify({"error": "Unauthorized"}), 401

  init_db()
  conn = sqlite3.connect(DB_FILE)
  conn.row_factory = sqlite3.Row
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM responses")
  rows = cursor.fetchall()
  conn.close()

  formatted_rows = []
  for row in rows:
    formatted_rows.append({
        "Name": row["name"],
        "Gmail": row["gmail"],
        "Language": row["language"],
        "Q1_Education": row["q1_education"],
        "Q2_Status": row["q2_status"],
        "Q3_Field": row["q3_field"],
        "Q4_Challenge": row["q4_challenge"],
        "Q5_Sufficiency": row["q5_sufficiency"],
        "Q6_Gap": row["q6_gap"],
        "Q7_Confidence": row["q7_confidence"],
        "Q8_Importance": row["q8_importance"],
        "Q9_Format": row["q9_format"],
        "Q10_Time": row["q10_time"],
        "Q11_Duration": row["q11_duration"],
        "Q12_Investment": row["q12_investment"],
        "Q13_Payment": row["q13_payment"],
        "Q14_Priority": row["q14_priority"],
        "Q15_Interest": row["q15_interest"],
        "Q16_Problem": row["q16_problem"],
    })

  return jsonify(formatted_rows)


@app.route("/clear_data", methods=["POST"])
def clear_data():
  if not session.get("logged_in"):
    return jsonify({"error": "Unauthorized"}), 401

  conn = sqlite3.connect(DB_FILE)
  cursor = conn.cursor()
  cursor.execute("DELETE FROM responses")
  conn.commit()
  conn.close()
  return jsonify({"status": "success"})


@app.route("/submit", methods=["POST"])
def submit():
  data = request.json
  init_db()

  conn = sqlite3.connect(DB_FILE)
  cursor = conn.cursor()
  cursor.execute(
      """
        INSERT INTO responses (
            name, gmail, language, q1_education, q2_status, q3_field, 
            q4_challenge, q5_sufficiency, q6_gap, q7_confidence, 
            q8_importance, q9_format, q10_time, q11_duration, 
            q12_investment, q13_payment, q14_priority, q15_interest, q16_problem
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
      (
          data.get("Name"),
          data.get("Gmail", "Not Provided"),
          data.get("Language"),
          data.get("Q1_Education"),
          data.get("Q2_Status"),
          data.get("Q3_Field"),
          data.get("Q4_Challenge"),
          data.get("Q5_Sufficiency"),
          data.get("Q6_Gap"),
          data.get("Q7_Confidence"),
          data.get("Q8_Importance"),
          data.get("Q9_Format"),
          data.get("Q10_Time"),
          data.get("Q11_Duration"),
          data.get("Q12_Investment"),
          data.get("Q13_Payment"),
          data.get("Q14_Priority"),
          data.get("Q15_Interest"),
          data.get("Q16_Problem", "Not Provided"),
      ),
  )
  conn.commit()
  conn.close()

  return jsonify({"status": "success", "message": "Saved to database successfully!"})


if __name__ == "__main__":
  init_db()
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)