import pandas as pd
import streamlit as st

def authenticate(username, password):
    users = pd.read_csv("data/users.csv")
    user = users[(users["Username"] == username) & (users["Password"] == password)]
    if not user.empty:
        return dict(
            username=user.iloc[0]["Username"],
            email=user.iloc[0]["Email"],
            role=user.iloc[0]["Role"]
        )
    return None

def login_screen():
    st.sidebar.header("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        user = authenticate(username, password)
        if user:
            st.session_state["user"] = user
            st.success(f"Welcome, {user['username']}")
            st.rerun()
        else:
            st.error("Invalid credentials")

def logout_button():
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()
