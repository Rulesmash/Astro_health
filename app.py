import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
from flask import Flask, render_template, request

# Initialize Firebase
cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)

def astronaut_health(heart, sleep, water, stress):
    score = 100

    if heart > 100: score -= 20
    if sleep < 6: score -= 25
    if water < 2: score -= 15
    if stress > 3: score -= 20

    if score >= 70:
        status = "Safe ✅"
    elif score >= 40:
        status = "Warning ⚠️"
    else:
        status = "Critical ❌"

    return score, status

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        heart = int(request.form["heart"])
        sleep = int(request.form["sleep"])
        water = int(request.form["water"])
        stress = int(request.form["stress"])

        score, status = astronaut_health(heart, sleep, water, stress)
        return render_template("index.html", score=score, status=status)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
