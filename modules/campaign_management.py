#Create marketing campaigns (social media, email, ads)
#Track campaign name, type, start/end date, budget, results
#Connect with APIs (Meta Ads, Google Ads, Mailchimp)

import sqlite3
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.config import DB_PATH

def create_campaign(client_id, name, type, budget, start_date, end_date):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO campaigns (client_id,name,type,budget,start_date,end_date,status)
    VALUES (?,?,?,?,?,?,'Running')""",
                   (client_id,name,type,budget,start_date,end_date))
    conn.commit()
    conn.close()

def get_campaigns(client_id=None):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Return rows as dictionary-like objects
    cursor = conn.cursor()
    if client_id:
        cursor.execute("SELECT * FROM campaigns WHERE client_id=?", (client_id,))
    else:
        cursor.execute("SELECT * FROM campaigns")
    rows = cursor.fetchall()
    conn.close()
    # Convert Row objects to plain dictionaries
    return [dict(row) for row in rows]
