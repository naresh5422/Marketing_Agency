
import os
import sys
import streamlit as st
from dashboards import client_dashboard, campaign_dashboard
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
st.set_page_config(page_title="Marketing Agency", layout="wide")
st.title("Marketing Agency Dashboard")

menu = ["Clients", "Campaigns"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Clients":
    client_dashboard.show()
elif choice == "Campaigns":
    campaign_dashboard.show()
