from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_file
)

import os
import json
import joblib
import numpy as np

from datetime import datetime

from generate_report import generate_pdf
from chart_generator import generate_charts

# ==========================================================
# Flask App
# ==========================================================

app = Flask(__name__)
app.secret_key = "heart_disease_secret_key"

# ==========================================================
# Folders
# ==========================================================

DATA_FOLDER = "data"
REPORT_FOLDER = "reports"

PATIENT_FILE = os.path.join(DATA_FOLDER, "patients.json")
PROFILE_FILE = os.path.join(DATA_FOLDER, "profile.json")
SETTINGS_FILE = os.path.join(DATA_FOLDER, "settings.json")

os.makedirs(DATA_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

# ==========================================================
# Load ML Model
# ==========================================================

model = joblib.load("heart_model.pkl")
scaler = joblib.load("scaler.pkl")

# ==========================================================
# Create JSON Files (First Run)
# ==========================================================

if not os.path.exists(PATIENT_FILE):
    with open(PATIENT_FILE, "w") as f:
        json.dump([], f, indent=4)

if not os.path.exists(PROFILE_FILE):
    with open(PROFILE_FILE, "w") as f:
        json.dump(
            {
                "name": "Nishu",
                "email": "",
                "phone": "",
                "address": "",
                "avatar": "avatar.png"
            },
            f,
            indent=4
        )

if not os.path.exists(SETTINGS_FILE):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(
            {
                "theme": "light",
                "notifications": True
            },
            f,
            indent=4
        )

# ==========================================================
# Helper Functions
# ==========================================================

def get_all_patients():
    with open(PATIENT_FILE, "r") as f:
        return json.load(f)


def save_all_patients(patients):
    with open(PATIENT_FILE, "w") as f:
        json.dump(patients, f, indent=4)


def load_profile():
    with open(PROFILE_FILE, "r") as f:
        return json.load(f)


def save_profile(profile):
    with open(PROFILE_FILE, "w") as f:
        json.dump(profile, f, indent=4)


def load_settings():
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)


def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)


def get_patient_by_id(patient_id):

    patients = get_all_patients()

    for patient in patients:
        if patient["id"] == patient_id:
            return patient

    return None
@app.context_processor
def inject_settings():
    return {
        "settings": load_settings()
    }
# ==========================================================
# DASHBOARD
# ==========================================================

@app.route("/")
@app.route("/dashboard")
def dashboard():

    patients = get_all_patients()

    total_patients = len(patients)

    total_predictions = sum(
        1 for p in patients
        if p.get("prediction")
    )

    high_risk = sum(
        1 for p in patients
        if p.get("prediction", {}).get("risk") == "High Risk"
    )

    low_risk = sum(
        1 for p in patients
        if p.get("prediction", {}).get("risk") == "Low Risk"
    )

    return render_template(

        "dashboard.html",

        active_page="dashboard",

        profile=load_profile(),

        total_patients=total_patients,

        total_predictions=total_predictions,

        high_risk=high_risk,

        low_risk=low_risk

    )


# ==========================================================
# PATIENT REGISTRATION
# ==========================================================

@app.route("/registration", methods=["GET", "POST"])
def registration():

    if request.method == "POST":

        patients = get_all_patients()

        patient_id = patients[-1]["id"] + 1 if patients else 1

        patient = {

            "id": patient_id,

            "name": request.form["name"],

            "age": int(request.form["age"]),

            "gender": request.form["gender"],

            "blood_group": request.form["blood_group"],

            "phone": request.form["phone"],

            "email": request.form["email"],

            "address": request.form["address"],

            "emergency_contact": request.form["emergency_contact"],

            "registered_on": datetime.now().strftime("%d-%m-%Y"),

            "prediction": {}

        }

        patients.append(patient)

        save_all_patients(patients)

        flash("Patient Registered Successfully!", "success")

        return redirect(url_for("registration"))

    patients = get_all_patients()

    patient_id = patients[-1]["id"] + 1 if patients else 1

    today = datetime.now().strftime("%d-%m-%Y")

    return render_template(

        "registration.html",

        active_page="registration",

        profile=load_profile(),

        patient=None,

        patient_id=patient_id,

        today=today

    )


# ==========================================================
# PREDICTION PAGE
# ==========================================================

@app.route("/prediction")
def prediction():

    patients = get_all_patients()

    return render_template(

        "prediction.html",

        active_page="prediction",

        profile=load_profile(),

        patients=patients

    )
# ==========================================================
# PREDICT HEART DISEASE
# ==========================================================

@app.route("/predict", methods=["POST"])
def predict():

    patients = get_all_patients()

    patient_id = int(request.form["patient_id"])

    patient = get_patient_by_id(patient_id)

    if patient is None:

        flash("Patient not found!", "danger")

        return redirect(url_for("prediction"))

    # -------------------------
    # Patient Details
    # -------------------------

    age = patient["age"]

    sex = 1 if patient["gender"].lower() == "male" else 0

    # -------------------------
    # Medical Parameters
    # -------------------------

    cp = int(request.form["cp"])
    trestbps = int(request.form["trestbps"])
    chol = int(request.form["chol"])
    fbs = int(request.form["fbs"])
    restecg = int(request.form["restecg"])
    thalach = int(request.form["thalach"])
    exang = int(request.form["exang"])
    oldpeak = float(request.form["oldpeak"])
    slope = int(request.form["slope"])
    ca = int(request.form["ca"])
    thal = int(request.form["thal"])

    # -------------------------
    # Model Input (13 Features)
    # -------------------------

    data = np.array([[
        age,
        sex,
        cp,
        trestbps,
        chol,
        fbs,
        restecg,
        thalach,
        exang,
        oldpeak,
        slope,
        ca,
        thal
    ]])

    scaled = scaler.transform(data)

    prediction = model.predict(scaled)[0]

    probability = round(
        model.predict_proba(scaled)[0][1] * 100,
        2
    )

    if prediction == 1:

        risk = "High Risk"

        recommendation = (
            "Consult a cardiologist immediately. "
            "Maintain a healthy diet, exercise regularly, "
            "and schedule regular check-ups."
        )

    else:

        risk = "Low Risk"

        recommendation = (
            "Maintain a healthy lifestyle and continue regular exercise."
        )

    # -------------------------
    # Save Prediction
    # -------------------------

    for p in patients:

        if p["id"] == patient_id:

            p["prediction"] = {

                "risk": risk,

                "probability": probability,

                "prediction_date": datetime.now().strftime("%d-%m-%Y"),

                "parameters": {

                    "cp": cp,
                    "trestbps": trestbps,
                    "chol": chol,
                    "fbs": fbs,
                    "restecg": restecg,
                    "thalach": thalach,
                    "exang": exang,
                    "oldpeak": oldpeak,
                    "slope": slope,
                    "ca": ca,
                    "thal": thal

                }

            }

            break

    save_all_patients(patients)

    # Generate chart for all patients
    generate_charts(patients)

    flash("Prediction Completed Successfully!", "success")

    return render_template(

        "prediction.html",

        active_page="prediction",

        profile=load_profile(),

        patients=patients,

        prediction=risk,

        probability=probability,

        recommendation=recommendation,

        selected_patient=patient

    )


# ==========================================================
# REPORTS
# ==========================================================

@app.route("/reports")
def reports():

    patients = get_all_patients()

    return render_template(

        "reports.html",

        active_page="reports",

        profile=load_profile(),

        patients=patients

    )
# ==========================================================
# RESULT PAGE
# ==========================================================

@app.route("/patient/<int:patient_id>")
def patient_report(patient_id):

    patient = get_patient_by_id(patient_id)

    if patient is None:

        flash("Patient not found!", "danger")

        return redirect(url_for("reports"))

    return render_template(

        "result.html",

        active_page="reports",

        profile=load_profile(),

        patient=patient

    )


# ==========================================================
# DOWNLOAD PDF REPORT
# ==========================================================

@app.route("/download_report/<int:patient_id>")
def download_report(patient_id):

    patient = get_patient_by_id(patient_id)

    if patient is None:

        flash("Patient not found!", "danger")

        return redirect(url_for("reports"))

    pdf_path = generate_pdf(patient)

    return send_file(

        pdf_path,

        as_attachment=True

    )


# ==========================================================
# ANALYTICS
# ==========================================================

@app.route("/analytics")
def analytics():

    patients = get_all_patients()

    predicted_patients = [

        p for p in patients

        if p.get("prediction")

    ]

    total_patients = len(patients)

    total_predictions = len(predicted_patients)

    high_risk = sum(

        1 for p in predicted_patients

        if p["prediction"]["risk"] == "High Risk"

    )

    low_risk = sum(

        1 for p in predicted_patients

        if p["prediction"]["risk"] == "Low Risk"

    )

    if total_predictions > 0:

        average_probability = round(

            sum(

                p["prediction"]["probability"]

                for p in predicted_patients

            ) / total_predictions,

            2

        )

    else:

        average_probability = 0

    generate_charts(predicted_patients)

    return render_template(

        "analytics.html",

        active_page="analytics",

        profile=load_profile(),

        patients=predicted_patients,

        total_patients=total_patients,

        total_predictions=total_predictions,

        high_risk=high_risk,

        low_risk=low_risk,

        average_probability=average_probability

    )
# ==========================================================
# PROFILE
# ==========================================================

@app.route("/profile")
def profile():

    return render_template(

        "profile.html",

        active_page="profile",

        profile=load_profile()

    )


@app.route("/update_profile", methods=["POST"])
def update_profile():

    profile = {

        "name": request.form["name"],

        "email": request.form["email"],

        "phone": request.form["phone"],

        "address": request.form["address"],

        "avatar": "avatar.png"

    }

    save_profile(profile)

    flash("Profile Updated Successfully!", "success")

    return redirect(url_for("profile"))


# ==========================================================
# SETTINGS
# ==========================================================

@app.route("/settings")
def settings():

    return render_template(

        "settings.html",

        active_page="settings",

        profile=load_profile(),

        settings=load_settings()

    )


@app.route("/save_settings", methods=["POST"])
def save_settings_route():

    settings = {

        "theme": request.form["theme"],

        "notifications": "notifications" in request.form

    }

    save_settings(settings)

    flash("Settings Saved Successfully!", "success")

    return redirect(url_for("settings"))


# ==========================================================
# EDIT PATIENT
# ==========================================================

@app.route("/edit_patient/<int:patient_id>")
def edit_patient(patient_id):

    patient = get_patient_by_id(patient_id)

    if patient is None:

        flash("Patient not found!", "danger")

        return redirect(url_for("reports"))

    return render_template(

        "registration.html",

        active_page="registration",

        profile=load_profile(),

        patient=patient,

        patient_id=patient["id"],

        today=patient["registered_on"]

    )


# ==========================================================
# UPDATE PATIENT
# ==========================================================

@app.route("/update_patient/<int:patient_id>", methods=["POST"])
def update_patient(patient_id):

    patients = get_all_patients()

    for patient in patients:

        if patient["id"] == patient_id:

            patient["name"] = request.form["name"]
            patient["age"] = int(request.form["age"])
            patient["gender"] = request.form["gender"]
            patient["blood_group"] = request.form["blood_group"]
            patient["phone"] = request.form["phone"]
            patient["email"] = request.form["email"]
            patient["address"] = request.form["address"]
            patient["emergency_contact"] = request.form["emergency_contact"]

            break

    save_all_patients(patients)

    flash("Patient Updated Successfully!", "success")

    return redirect(url_for("reports"))


# ==========================================================
# DELETE PATIENT
# ==========================================================

@app.route("/delete_patient/<int:patient_id>")
def delete_patient(patient_id):

    patients = get_all_patients()

    patients = [

        patient

        for patient in patients

        if patient["id"] != patient_id

    ]

    save_all_patients(patients)

    flash("Patient Deleted Successfully!", "warning")

    return redirect(url_for("reports"))


# ==========================================================
# RUN APPLICATION
# ==========================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )
    