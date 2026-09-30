import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def create_ai_report_pdf(report_id, ai_report_text, output_folder="pdf_reports"):
    os.makedirs(output_folder, exist_ok=True)

    pdf_path = f"{output_folder}/{report_id}_ai_report.pdf"

    document = SimpleDocTemplate(
        pdf_path,
        pagesize=A4
    )

    styles = getSampleStyleSheet()

    story = []

    title = Paragraph(
        f"InsightFlow AI Report - {report_id}",
        styles["Title"]
    )

    story.append(title)
    story.append(Spacer(1, 20))

    lines = ai_report_text.split("\n")

    for line in lines:
        clean_line = line.strip()

        if clean_line:
            paragraph = Paragraph(
                clean_line,
                styles["BodyText"]
            )
            story.append(paragraph)
            story.append(Spacer(1, 8))

    document.build(story)

    return pdf_path.replace("\\", "/")