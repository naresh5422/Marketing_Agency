import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
from automation.auth_manager import login_screen, logout_button
from dashboards import roadmap_dashboard, admin_dashboard, client_dashboard, campaign_dashboard
from automation.scheduler import start_scheduler

st.set_page_config(page_title="Marketing Agency Dashboard", layout="wide")
st.title("Marketing Agency Control Center")

menu = ["Clients", "Campaigns", "Roadmap Tracker"]
choice = st.sidebar.selectbox("Menu", menu)
# choice = st.sidebar.radio("Select Module", menu)
if choice == "Clients":
    client_dashboard.show()
elif choice == "Campaigns":
    campaign_dashboard.show()
elif choice == "Roadmap Tracker":
    if "user" not in st.session_state:
        login_screen()
    else:
        user = st.session_state["user"]
        logout_button()
        start_scheduler()

        if user["role"].lower() == "admin":
            st.sidebar.title("Admin Panel")
            page = st.sidebar.radio("Choose View", ["Roadmap Tracker", "Admin Analytics"])
            if page == "Roadmap Tracker":
                roadmap_dashboard.show()
            else:
                admin_dashboard.show_admin_dashboard()
        else:
            roadmap_dashboard.show()
