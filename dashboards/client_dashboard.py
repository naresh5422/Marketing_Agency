import streamlit as st
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.client_management import get_cached_clients, add_client

def show():
    st.subheader("Clients")
    clients = get_cached_clients()
    for c in clients:
        st.write(f"{c['id']} - {c['name']} ({c['company']}) - Retainer: {c['retainer_fee']}")

    st.subheader("Add New Client")
    with st.form("add_client"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        company = st.text_input("Company")
        retainer = st.number_input("Retainer Fee", 0)
        join_date = st.date_input("Join Date")
        submitted = st.form_submit_button("Add Client")
        if submitted:
            add_client(name,email,company,retainer,str(join_date))
            get_cached_clients.clear()
            st.rerun()
            st.success("Client added successfully!")
