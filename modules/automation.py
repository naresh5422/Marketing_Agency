#Schedule emails, reminders, and posts
#Use schedule + smtplib or API integrations
#Optional: connect with social media APIs
import os
import sys
import schedule
import time
import smtplib

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from modules.reporting import generate_excel_report
from modules.campaign_management import get_campaigns
from modules.analytics import calculate_roi
from config.config import LOG_FILE
import logging

# Logging setup
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# -------- Email Automation --------
def send_email(to_email, subject, body, attachment_path=None):
    sender_email = "youragency@example.com"
    password = "yourpassword"  # For Gmail, use app password
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    if attachment_path:
        from email.mime.base import MIMEBase
        from email import encoders
        with open(attachment_path, "rb") as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={attachment_path.split("/")[-1]}')
        msg.attach(part)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)
        server.quit()
        logging.info(f"Email sent to {to_email}")
    except Exception as e:
        logging.error(f"Error sending email: {e}")

# -------- Daily Client Report Job --------
def daily_client_report_job():
    from modules.client_management import get_clients
    clients = get_clients()
    for client in clients:
        report_path = generate_excel_report(client['id'])
        body = f"Hello {client['name']},\n\nPlease find attached your latest campaign report.\n\nRegards,\nMarketing Agency"
        send_email(client['email'], "Daily Campaign Report", body, report_path)

# -------- Simulated Social Media Post Scheduler --------
def post_social_media(campaign_name, content, platform):
    logging.info(f"Posting '{campaign_name}' to {platform}: {content[:50]}...")
    print(f"[SIMULATION] Posted '{campaign_name}' to {platform}")

def schedule_social_posts():
    campaigns = get_campaigns()
    for c in campaigns:
        post_social_media(c[2], f"Promo content for {c[2]}", "Facebook")
        post_social_media(c[2], f"Promo content for {c[2]}", "Instagram")

# -------- Scheduling Jobs --------
def start_scheduled_jobs():
    schedule.every().day.at("08:00").do(daily_client_report_job)
    schedule.every().hour.do(schedule_social_posts)  # every hour simulation

    while True:
        schedule.run_pending()
        time.sleep(60)
