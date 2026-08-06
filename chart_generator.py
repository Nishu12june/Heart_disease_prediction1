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

    predicted = [
        p for p in patients
        if p.get("prediction") and p["prediction"].get("risk")
    ]

    # -------------------------
    # No prediction available
    # -------------------------
    if len(predicted) == 0:
        return

    # -------------------------
    # Risk Distribution Pie Chart
    # -------------------------
    high = sum(
        1 for p in predicted
        if p["prediction"]["risk"] == "High Risk"
    )

    low = sum(
        1 for p in predicted
        if p["prediction"]["risk"] == "Low Risk"
    )

    plt.figure(figsize=(5, 5))

    plt.pie(
        [high, low],
        labels=["High Risk", "Low Risk"],
        autopct="%1.1f%%",
        startangle=90
    )

    plt.title("Risk Distribution")

    plt.savefig(
        os.path.join(CHART_FOLDER, "risk_distribution.png"),
        bbox_inches="tight"
    )

    plt.close()

    # -------------------------
    # Patient-wise Probability Chart
    # -------------------------

    names = [p["name"] for p in predicted]

    probabilities = [
        p["prediction"]["probability"]
        for p in predicted
    ]

    plt.figure(figsize=(8, 5))

    plt.bar(names, probabilities)

    plt.title("Patient Risk Probability")

    plt.xlabel("Patients")

    plt.ylabel("Probability (%)")

    plt.xticks(rotation=30)

    plt.tight_layout()

    plt.savefig(
        os.path.join(CHART_FOLDER, "probability_chart.png")
    )

    plt.close()

    # -------------------------
    # Individual Patient Charts
    # -------------------------

    for patient in predicted:

        plt.figure(figsize=(4, 4))

        plt.bar(
            ["Risk"],
            [patient["prediction"]["probability"]]
        )

        plt.ylim(0, 100)

        plt.ylabel("Probability (%)")

        plt.title(
            f'{patient["name"]} ({patient["prediction"]["risk"]})'
        )

        filename = f'patient_{patient["id"]}.png'

        plt.tight_layout()

        plt.savefig(
            os.path.join(CHART_FOLDER, filename)
        )

        plt.close()