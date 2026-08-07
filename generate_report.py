<<<<<<< HEAD
import os
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
)

REPORT_FOLDER = "reports"
CHART_FOLDER = "static/charts"

os.makedirs(REPORT_FOLDER, exist_ok=True)


def generate_pdf(patient):

    pdf_path = os.path.join(
        REPORT_FOLDER,
        f"Patient_{patient['id']}.pdf"
    )

    doc = SimpleDocTemplate(pdf_path)

    styles = getSampleStyleSheet()

    story = []

    # -----------------------------
    # Title
    # -----------------------------
    story.append(
        Paragraph(
            "<b><font size=18>Heart Disease Prediction Report</font></b>",
            styles["Title"],
        )
    )

    story.append(Spacer(1, 20))

    # -----------------------------
    # Patient Information
    # -----------------------------
    story.append(
        Paragraph("<b>Patient Information</b>", styles["Heading2"])
    )

    data = [

        ["Patient ID", patient["id"]],
        ["Name", patient["name"]],
        ["Age", patient["age"]],
        ["Gender", patient["gender"]],
        ["Blood Group", patient["blood_group"]],
        ["Phone", patient["phone"]],
        ["Email", patient["email"]],
        ["Address", patient["address"]],
        ["Emergency Contact", patient["emergency_contact"]],
        ["Registered On", patient["registered_on"]],

    ]

    table = Table(data, colWidths=[160, 300])

    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("BACKGROUND", (0, 0), (0, -1), colors.whitesmoke),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ])
    )

    story.append(table)

    story.append(Spacer(1, 20))

    # -----------------------------
    # Prediction
    # -----------------------------
    prediction = patient.get("prediction", {})

    if prediction:

        story.append(
            Paragraph("<b>Prediction Result</b>", styles["Heading2"])
        )

        risk = prediction.get("risk", "Pending")
        probability = prediction.get("probability", 0)

        pdata = [

            ["Risk", risk],
            ["Probability", f"{probability}%"],

        ]

        ptable = Table(pdata, colWidths=[160, 300])

        ptable.setStyle(
            TableStyle([
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("BACKGROUND", (0, 0), (0, -1), colors.whitesmoke),
            ])
        )

        story.append(ptable)

        story.append(Spacer(1, 20))

        # -----------------------------
        # Medical Parameters
        # -----------------------------
        params = prediction.get("parameters", {})

        if params:

            story.append(
                Paragraph("<b>Medical Parameters</b>", styles["Heading2"])
            )

            mdata = []

            for key, value in params.items():
                mdata.append([key.upper(), str(value)])

            mtable = Table(mdata, colWidths=[180, 280])

            mtable.setStyle(
                TableStyle([
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ("BACKGROUND", (0, 0), (0, -1), colors.whitesmoke),
                ])
            )

            story.append(mtable)

            story.append(Spacer(1, 20))

        # -----------------------------
        # Patient Chart
        # -----------------------------
        chart = os.path.join(
            CHART_FOLDER,
            f"patient_{patient['id']}.png"
        )

        if os.path.exists(chart):

            story.append(
                Paragraph("<b>Risk Analysis Chart</b>", styles["Heading2"])
            )

            story.append(Image(chart, width=350, height=250))

            story.append(Spacer(1, 20))

    else:

        story.append(
            Paragraph(
                "<b>No prediction available for this patient.</b>",
                styles["Heading2"],
            )
        )

    # -----------------------------
    # Recommendation
    # -----------------------------
    story.append(
        Paragraph("<b>Recommendation</b>", styles["Heading2"])
    )

    if prediction:

        if prediction["risk"] == "High Risk":

            text = """
            • Immediate consultation with a cardiologist is recommended.<br/>
            • Maintain a healthy diet.<br/>
            • Exercise regularly.<br/>
            • Monitor blood pressure and cholesterol.<br/>
            • Avoid smoking and alcohol.
            """

        else:

            text = """
            • Continue a healthy lifestyle.<br/>
            • Exercise regularly.<br/>
            • Maintain balanced nutrition.<br/>
            • Schedule routine health checkups.
            """

    else:

        text = "Prediction has not been performed."

    story.append(
        Paragraph(text, styles["BodyText"])
    )

    doc.build(story)

=======
import os
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
)

REPORT_FOLDER = "reports"
CHART_FOLDER = "static/charts"

os.makedirs(REPORT_FOLDER, exist_ok=True)


def generate_pdf(patient):

    pdf_path = os.path.join(
        REPORT_FOLDER,
        f"Patient_{patient['id']}.pdf"
    )

    doc = SimpleDocTemplate(pdf_path)

    styles = getSampleStyleSheet()

    story = []

    # -----------------------------
    # Title
    # -----------------------------
    story.append(
        Paragraph(
            "<b><font size=18>Heart Disease Prediction Report</font></b>",
            styles["Title"],
        )
    )

    story.append(Spacer(1, 20))

    # -----------------------------
    # Patient Information
    # -----------------------------
    story.append(
        Paragraph("<b>Patient Information</b>", styles["Heading2"])
    )

    data = [

        ["Patient ID", patient["id"]],
        ["Name", patient["name"]],
        ["Age", patient["age"]],
        ["Gender", patient["gender"]],
        ["Blood Group", patient["blood_group"]],
        ["Phone", patient["phone"]],
        ["Email", patient["email"]],
        ["Address", patient["address"]],
        ["Emergency Contact", patient["emergency_contact"]],
        ["Registered On", patient["registered_on"]],

    ]

    table = Table(data, colWidths=[160, 300])

    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("BACKGROUND", (0, 0), (0, -1), colors.whitesmoke),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ])
    )

    story.append(table)

    story.append(Spacer(1, 20))

    # -----------------------------
    # Prediction
    # -----------------------------
    prediction = patient.get("prediction", {})

    if prediction:

        story.append(
            Paragraph("<b>Prediction Result</b>", styles["Heading2"])
        )

        risk = prediction.get("risk", "Pending")
        probability = prediction.get("probability", 0)

        pdata = [

            ["Risk", risk],
            ["Probability", f"{probability}%"],

        ]

        ptable = Table(pdata, colWidths=[160, 300])

        ptable.setStyle(
            TableStyle([
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("BACKGROUND", (0, 0), (0, -1), colors.whitesmoke),
            ])
        )

        story.append(ptable)

        story.append(Spacer(1, 20))

        # -----------------------------
        # Medical Parameters
        # -----------------------------
        params = prediction.get("parameters", {})

        if params:

            story.append(
                Paragraph("<b>Medical Parameters</b>", styles["Heading2"])
            )

            mdata = []

            for key, value in params.items():
                mdata.append([key.upper(), str(value)])

            mtable = Table(mdata, colWidths=[180, 280])

            mtable.setStyle(
                TableStyle([
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ("BACKGROUND", (0, 0), (0, -1), colors.whitesmoke),
                ])
            )

            story.append(mtable)

            story.append(Spacer(1, 20))

        # -----------------------------
        # Patient Chart
        # -----------------------------
        chart = os.path.join(
            CHART_FOLDER,
            f"patient_{patient['id']}.png"
        )

        if os.path.exists(chart):

            story.append(
                Paragraph("<b>Risk Analysis Chart</b>", styles["Heading2"])
            )

            story.append(Image(chart, width=350, height=250))

            story.append(Spacer(1, 20))

    else:

        story.append(
            Paragraph(
                "<b>No prediction available for this patient.</b>",
                styles["Heading2"],
            )
        )

    # -----------------------------
    # Recommendation
    # -----------------------------
    story.append(
        Paragraph("<b>Recommendation</b>", styles["Heading2"])
    )

    if prediction:

        if prediction["risk"] == "High Risk":

            text = """
            • Immediate consultation with a cardiologist is recommended.<br/>
            • Maintain a healthy diet.<br/>
            • Exercise regularly.<br/>
            • Monitor blood pressure and cholesterol.<br/>
            • Avoid smoking and alcohol.
            """

        else:

            text = """
            • Continue a healthy lifestyle.<br/>
            • Exercise regularly.<br/>
            • Maintain balanced nutrition.<br/>
            • Schedule routine health checkups.
            """

    else:

        text = "Prediction has not been performed."

    story.append(
        Paragraph(text, styles["BodyText"])
    )

    doc.build(story)

>>>>>>> d85dfd8f2628d11e6b3f4ea3933703c11539184f
    return pdf_path