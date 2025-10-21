import os
import sys
from dotenv import load_dotenv
import sqlite3

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.config import DB_PATH

load_dotenv()
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Clients Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT,
    company TEXT,
    retainer_fee REAL,
    join_date TEXT
)
""")

# Campaigns Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS campaigns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER,
    name TEXT,
    type TEXT,
    budget REAL,
    start_date TEXT,
    end_date TEXT,
    spend REAL DEFAULT 0,
    revenue REAL DEFAULT 0,
    status TEXT,
    FOREIGN KEY(client_id) REFERENCES clients(id)
)
""")

conn.commit()
conn.close()
print("Database and tables created.")
