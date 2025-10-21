import os
import sys
import sqlite3
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.config import DB_PATH
load_dotenv()
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Add sample clients
clients = [
    ("Alice Johnson", "alice@example.com", "TechCorp", 5000, "2025-01-01"),
    ("Bob Smith", "bob@example.com", "MarketPlus", 3000, "2025-02-01")
]
cursor.executemany("INSERT INTO clients (name,email,company,retainer_fee,join_date) VALUES (?,?,?,?,?)", clients)

# Add sample campaigns
campaigns = [
    (1, "Q4 Social Media Blitz", "Social Media", 1500, "2025-10-01", "2025-12-31", 1200, 1800, "Running"),
    (1, "Black Friday Email Campaign", "Email", 500, "2025-11-20", "2025-11-30", 500, 1500, "Completed"),
    (1, "New Year Content Push", "Content Marketing", 800, "2026-01-01", "2026-01-31", 150, 0, "Planned"),
    (2, "Summer Google Ads", "Paid Ads", 2000, "2025-06-01", "2025-08-31", 1800, 3200, "Completed"),
    (2, "Website SEO Overhaul", "SEO", 1200, "2025-07-01", "2025-12-31", 600, 0, "Running")
]
cursor.executemany("""
INSERT INTO campaigns 
(client_id,name,type,budget,start_date,end_date,spend,revenue,status) 
VALUES (?,?,?,?,?,?,?,?,?)""", campaigns)

conn.commit()
conn.close()
print("Sample data loaded.")
