import csv
import os
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
DATA_FILE = "survey_responses.csv"


def init_csv():
  if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, mode="w", newline="", encoding="utf-8") as f:
      writer = csv.writer(f)
      writer.writerow([
          "Name",
          "Gmail",
          "Language",
          "Q1_Education",
          "Q2_Status",
          "Q3_Field",
          "Q4_Challenge",
          "Q5_Sufficiency",
          "Q6_Gap",
          "Q7_Confidence",
          "Q8_Importance",
          "Q9_Format",
          "Q10_Time",
          "Q11_Duration",
          "Q12_Investment",
          "Q13_Payment",
          "Q14_Priority",
          "Q15_Interest",
          "Q16_Problem",
      ])


@app.route("/")
def index():
  return render_template("index.html")


@app.route("/admin")
def admin_portal():
  return render_template("admin.html")


@app.route("/get_data")
def get_data():
  init_csv()
  rows = []
  with open(DATA_FILE, mode="r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
      rows.append(row)
  return jsonify(rows)


@app.route("/submit", methods=["POST"])
def submit():
  data = request.json
  init_csv()

  with open(DATA_FILE, mode="a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
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
    ])

  return jsonify({"status": "success", "message": "Saved successfully!"})


if __name__ == "__main__":
  init_csv()
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)