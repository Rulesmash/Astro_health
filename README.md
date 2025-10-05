# 🌌 AstroHealth AI  
### *AI-Powered Astronaut Health Monitoring System* 🚀  

![banner](https://i.imgur.com/BwW9YrL.jpeg)

> 🧠 An intelligent, space-themed web app that monitors astronaut vitals, predicts health risks, and offers personalized suggestions — built in just 24 hours for the NASA Space Hackathon 2025.

---

## 🪐 Inspiration

Astronauts on long-duration missions face physiological and psychological challenges — from increased heart rate to stress and temperature fluctuations in microgravity.  
We wanted to build a **simple AI-assisted system** that can track key vitals and provide **real-time insights and advice**, ensuring crew safety and mission continuity.

---

## 🚀 What It Does

**AstroHealth AI** is a web-based health monitor that:

- 🧭 Collects health parameters (Heart Rate, Blood Pressure, Stress, Temperature)  
- ⚙️ Analyzes health condition instantly using a Flask backend  
- 🧩 Saves logs to Firebase Firestore with timestamps  
- 💬 Generates smart suggestions for each abnormal vital  
- 📜 Displays previous health reports in a glowing space-themed dashboard  
- 🌠 Runs inside a Docker container for universal deployment  

---

## 🧑‍🚀 Tech Stack

| Layer | Technology |
|:------|:------------|
| **Frontend** | HTML, CSS (3D Space UI), Vanilla JS |
| **Backend** | Python (Flask) |
| **Database** | Firebase Firestore |
| **Hosting / Deploy** | Docker + Render |
| **Extras** | Gunicorn (for production server) |

---

## 🧰 Architecture Overview

+-----------------------------+
| Astronaut Dashboard |
| (HTML + CSS + JS + 3D UI) |
+--------------+--------------+
|
v
+-----------------------------+
| Flask Backend |
| - REST API for /analyse |
| - Suggestion Engine (AI) |
| - Report Logging |
+--------------+--------------+
|
v
+-----------------------------+
| Firebase Firestore |
| Cloud DB storing all logs |
+-----------------------------+
