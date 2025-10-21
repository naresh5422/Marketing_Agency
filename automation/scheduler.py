import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from apscheduler.schedulers.background import BackgroundScheduler
# from datetime import datetime
# import pandas as pd
# from automation.email_notifier import send_email

# def check_progress_and_notify():
#     df = pd.read_csv("data/roadmap.csv")

#     for _, row in df.iterrows():
#         month, goal, progress = row["Month"], row["Goal"], int(row["Progress"])
#         recipient = row.get("Email", "your_email@gmail.com")

#         if progress < 50:
#             subject = f"⚠️ Reminder: Low Progress for Month {month}"
#             body = f"As of {datetime.now().strftime('%Y-%m-%d')}, your progress for '{goal}' is only {progress}%. Consider reviewing tasks."
#             send_email(subject, body, recipient)

#         elif progress >= 100:
#             subject = f"✅ Completed: Month {month} Goal Achieved"
#             body = f"Nice work! You have completed your goal '{goal}' with {progress}% progress."
#             send_email(subject, body, recipient)

# def start_scheduler():
#     scheduler = BackgroundScheduler()
#     # Runs every Monday at 9 AM
#     scheduler.add_job(check_progress_and_notify, "cron", day_of_week="mon", hour=9, minute=0)
#     scheduler.start()
#     print("Scheduler started. Weekly reminders activated.")


from apscheduler.schedulers.background import BackgroundScheduler
from automation.monthly_report import send_monthly_admin_report
from automation.email_notifier import send_email
import pandas as pd

def weekly_team_reminder():
    df = pd.read_csv("data/roadmap.csv")
    for _, row in df.iterrows():
        recipient = row.get("Email", "your_email@gmail.com")
        progress = int(row["Progress"])
        if progress < 50:
            subject = f"⚠️ Weekly Reminder for {row['Username']}"
            body = f"Your goal '{row['Goal']}' for Month {row['Month']} is only {progress}% done."
            send_email(subject, body, row["Email"])
        elif progress >= 100:
            subject = f"✅ Completed: Month {int(row['month'])} Goal Achieved"
            body = f"Nice work! You have completed your goal {int(row['goal'])} with {progress}% progress."
            send_email(subject, body, recipient)

def start_scheduler():
    scheduler = BackgroundScheduler()
    # Weekly reminder
    scheduler.add_job(weekly_team_reminder, "cron", day_of_week="mon", hour=9, minute=0)
    # Monthly report to admin
    df_users = pd.read_csv("data/users.csv")
    admin_email = df_users[df_users["Role"].str.lower() == "admin"]["Email"].values[0]
    scheduler.add_job(lambda: send_monthly_admin_report(admin_email), "cron", day=1, hour=10, minute=0)
    scheduler.start()
