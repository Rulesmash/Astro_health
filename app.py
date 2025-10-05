from flask import Flask, request, jsonify, render_template, Response
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import csv
import json
import os

app = Flask(__name__)

# --- Firebase Setup ---
try:
    if os.getenv("FIREBASE_KEY_JSON"):
        firebase_key = json.loads(os.getenv("FIREBASE_KEY_JSON"))
        cred = credentials.Certificate(firebase_key)
    else:
        cred = credentials.Certificate("firebase-key.json")

    firebase_admin.initialize_app(cred)
    db = firestore.client()
except Exception as e:
    print("❌ Firebase initialization failed:", e)
    db = None

# --- Routes ---

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/analyse', methods=['POST'])
def analyse():
    try:
        data = request.get_json()

        heart_rate = float(data.get("heart_rate", 0))
        bp_systolic = float(data.get("bp_systolic", 0))
        bp_diastolic = float(data.get("bp_diastolic", 0))
        stress = float(data.get("stress", 0))
        temperature = float(data.get("temperature", 0))

        status = "Normal"
        issues = []
        suggestions = []

        if heart_rate < 60 or heart_rate > 100:
            status = "Alert"
            issues.append("Abnormal Heart Rate")
            suggestions.append("Try deep breathing or hydration")

        if bp_systolic < 90 or bp_systolic > 120 or bp_diastolic < 60 or bp_diastolic > 80:
            status = "Alert"
            issues.append("Abnormal Blood Pressure")
            suggestions.append("Take rest and hydrate")

        if stress > 6:
            status = "Alert"
            issues.append("High Stress")
            suggestions.append("Take a mindfulness break")

        if temperature > 37.5:
            status = "Alert"
            issues.append("High Temperature")
            suggestions.append("Cool down and report if it persists")

        report = {
            "heart_rate": heart_rate,
            "bp_systolic": bp_systolic,
            "bp_diastolic": bp_diastolic,
            "stress": stress,
            "temperature": temperature,
            "status": status,
            "issues": issues,
            "suggestions": suggestions,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        if db:
            db.collection("health_reports").add(report)

        return jsonify({
            "message": "Health report analyzed and saved.",
            "status": status,
            "issues": issues,
            "suggestions": suggestions
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/reports')
def get_reports():
    try:
        reports_ref = db.collection("health_reports").order_by("timestamp", direction=firestore.Query.DESCENDING)
        reports = [doc.to_dict() for doc in reports_ref.stream()]
        return render_template("reports.html", reports=reports)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/download/csv')
def download_csv():
    try:
        reports_ref = db.collection("health_reports").order_by("timestamp", direction=firestore.Query.DESCENDING)
        reports = [doc.to_dict() for doc in reports_ref.stream()]

        def generate():
            data = csv.StringIO()
            writer = csv.writer(data)

            # Write header
            writer.writerow(["Timestamp", "Heart Rate", "BP Systolic", "BP Diastolic", "Stress", "Temperature", "Status", "Issues"])
            yield data.getvalue()
            data.seek(0)
            data.truncate(0)

            # Write rows
            for r in reports:
                writer.writerow([
                    r.get("timestamp", ""),
                    r.get("heart_rate", ""),
                    r.get("bp_systolic", ""),
                    r.get("bp_diastolic", ""),
                    r.get("stress", ""),
                    r.get("temperature", ""),
                    r.get("status", ""),
                    ", ".join(r.get("issues", []))
                ])
                yield data.getvalue()
                data.seek(0)
                data.truncate(0)

        return Response(generate(), mimetype="text/csv",
                        headers={"Content-Disposition": "attachment; filename=astronaut_reports.csv"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/download/json')
def download_json():
    try:
        reports_ref = db.collection("health_reports").order_by("timestamp", direction=firestore.Query.DESCENDING)
        reports = [doc.to_dict() for doc in reports_ref.stream()]
        return jsonify(reports)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
