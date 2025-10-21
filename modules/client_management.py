# Add, update, remove clients
# Track client info: name, email, company, campaigns, retainer fee
# Store in SQLite/PostgreSQL


import sqlite3
import streamlit as st
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.config import DB_PATH

def add_client(name, email, company, retainer_fee, join_date):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO clients (name,email,company,retainer_fee,join_date) VALUES (?,?,?,?,?)",
                   (name,email,company,retainer_fee,join_date))
    conn.commit()
    conn.close()

def get_clients():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Return rows as dictionary-like objects
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clients")
    rows = cursor.fetchall()
    conn.close()
    # Convert Row objects to plain dictionaries
    return [dict(row) for row in rows]

@st.cache_data
def get_cached_clients():
    return get_clients()
