import matplotlib
matplotlib.use("Agg")

import os
import matplotlib.pyplot as plt


CHART_FOLDER = "static/charts"
os.makedirs(CHART_FOLDER, exist_ok=True)


def generate_charts(patients):
    """
    Generate charts from patient prediction data.
    """

    # Make sure patients is actually a list
    if not isinstance(patients, list):
        return

    # Get patients having valid prediction data
    predicted = []

    for p in patients:
        if not isinstance(p, dict):
            continue

        prediction = p.get("prediction")

        if not isinstance(prediction, dict):
            continue

        if prediction.get("risk"):
            predicted.append(p)

    # No prediction available
    if not predicted:
        return

    # =====================================================
    # 1. RISK DISTRIBUTION PIE CHART
    # =====================================================

    high = sum(
        1
        for p in predicted
        if p["prediction"].get("risk") == "High Risk"
    )

    low = sum(
        1
        for p in predicted
        if p["prediction"].get("risk") == "Low Risk"
    )

    # Only create pie chart if there is data
    if high + low > 0:

        plt.figure(figsize=(5, 5))

        plt.pie(
            [high, low],
            labels=["High Risk", "Low Risk"],
            autopct="%1.1f%%",
            startangle=90
        )

        plt.title("Risk Distribution")

        plt.savefig(
            os.path.join(
                CHART_FOLDER,
                "risk_distribution.png"
            ),
            bbox_inches="tight"
        )

        plt.close()

    # =====================================================
    # 2. PATIENT-WISE PROBABILITY CHART
    # =====================================================

    names = []

    probabilities = []

    for p in predicted:

        name = p.get("name", "Unknown")

        probability = p["prediction"].get(
            "probability",
            0
        )

        # Convert probability to number
        try:
            probability = float(probability)
        except (ValueError, TypeError):
            probability = 0

        names.append(name)
        probabilities.append(probability)

    if names:

        plt.figure(figsize=(8, 5))

        plt.bar(
            names,
            probabilities
        )

        plt.title("Patient Risk Probability")

        plt.xlabel("Patients")

        plt.ylabel("Probability (%)")

        plt.xticks(rotation=30)

        plt.tight_layout()

        plt.savefig(
            os.path.join(
                CHART_FOLDER,
                "probability_chart.png"
            )
        )

        plt.close()

    # =====================================================
    # 3. INDIVIDUAL PATIENT CHARTS
    # =====================================================

    for patient in predicted:

        probability = patient["prediction"].get(
            "probability",
            0
        )

        try:
            probability = float(probability)
        except (ValueError, TypeError):
            probability = 0

        patient_id = patient.get(
            "id",
            "unknown"
        )

        patient_name = patient.get(
            "name",
            "Unknown Patient"
        )

        risk = patient["prediction"].get(
            "risk",
            "Unknown"
        )

        plt.figure(figsize=(4, 4))

        plt.bar(
            ["Risk"],
            [probability]
        )

        plt.ylim(0, 100)

        plt.ylabel("Probability (%)")

        plt.title(
            f"{patient_name} ({risk})"
        )

        plt.tight_layout()

        filename = f"patient_{patient_id}.png"

        plt.savefig(
            os.path.join(
                CHART_FOLDER,
                filename
            )
        )

        plt.close()
