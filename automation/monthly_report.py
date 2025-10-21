import pandas as pd
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from automation.email_notifier import send_email
from datetime import datetime

def generate_monthly_pdf():
    df = pd.read_csv("data/roadmap.csv")
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setFont("Helvetica", 12)
    pdf.drawString(30, 750, f"Monthly Progress Report - {datetime.now().strftime('%B %Y')}")

    y = 720
    for _, row in df.iterrows():
        text = f"Month {row['Month']} | {row['Username']} | {row['Goal']} | {row['Progress']}%"
        pdf.drawString(30, y, text)
        y -= 20
        if y < 50:
            pdf.showPage()
            pdf.setFont("Helvetica", 12)
            y = 750

    pdf.save()
    buffer.seek(0)
    return buffer

def send_monthly_admin_report(admin_email):
    pdf_buffer = generate_monthly_pdf()
    send_email(
        subject=f"📈 Monthly Progress Report - {datetime.now().strftime('%B %Y')}",
        body="Please find attached the monthly progress report for all team members.",
        recipient=admin_email
    )
