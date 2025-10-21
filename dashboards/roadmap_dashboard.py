import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# import streamlit as st
# import pandas as pd
# import plotly.express as px
# from automation.email_notifier import send_email

# def show():
#     st.subheader("6-Month Marketing Agency Roadmap")
#     st.write("Track monthly goals, tasks, and progress visually.")

#     df = pd.read_csv("data/roadmap.csv")
#     df["Progress"] = df["Progress"].fillna(0)

#     # Editable progress input
#     selected_month = st.selectbox("Select Month", df["Month"])
#     new_progress = st.slider("Update Progress (%)", 0, 100,
#                              int(df.loc[df["Month"] == selected_month, "Progress"].values[0]))
#     email = st.text_input("Enter your email for milestone alerts", "your_email@gmail.com")
#     if st.button("Save Progress"):
#         df.loc[df["Month"] == selected_month, "Progress"] = new_progress
#         df.to_csv("data/roadmap.csv", index=False)
#         st.success("Progress updated successfully!")
#         goal = df.loc[df["Month"] == selected_month, "Goal"].values[0]

#         # Send alerts
#         if new_progress < 50:
#             subject = f"⚠️ Low Progress Alert for Month {selected_month}"
#             body = f"Your goal '{goal}' is below 50% completion. Current progress: {new_progress}%."
#             send_email(subject, body, email)

#         elif new_progress >= 100:
#             subject = f"✅ Milestone Completed for Month {selected_month}"
#             body = f"Congratulations! You have completed your goal '{goal}' for this month."
#             send_email(subject, body, email)


#     # Display roadmap table
#     st.subheader("Roadmap Overview")
#     st.dataframe(df)

#     # Progress chart
#     fig = px.bar(df, x="Month", y="Progress", text="Progress", color="Progress", 
#                  color_continuous_scale="Blues", title="Monthly Progress Overview"
#     )
#     st.plotly_chart(fig, use_container_width=True)

#     # Milestone detail view
#     st.subheader("Goal Details")
#     for _, row in df.iterrows():
#         with st.expander(f"Month {row['Month']}: {row['Goal']}"):
#             st.write("**Tasks:**", row["Tasks"])
#             st.progress(int(row["Progress"]) / 100)


# def show():
#     user = st.session_state["user"]
#     st.title(f"{user['username'].capitalize()}'s Roadmap")

#     df = pd.read_csv("data/roadmap.csv")

#     # Each user filters their tasks
#     if "Username" in df.columns:
#         df_user = df[df["Username"] == user["username"]].copy()
#     else:
#         df["Username"] = user["username"]
#         df["Email"] = user["email"]
#         df_user = df.copy()

#     selected_month = st.selectbox("Select Month", df_user["Month"])
#     progress = int(df_user.loc[df_user["Month"] == selected_month, "Progress"].values[0])
#     new_progress = st.slider("Update Progress (%)", 0, 100, progress)

#     if st.button("Save Progress"):
#         df.loc[(df["Month"] == selected_month) & (df["Username"] == user["username"]), "Progress"] = new_progress
#         df.to_csv("data/roadmap.csv", index=False)
#         st.success("Progress updated.")

#         goal = df_user.loc[df_user["Month"] == selected_month, "Goal"].values[0]
#         if new_progress < 50:
#             send_email(f"⚠️ Reminder: {user['username']} Low Progress", f"Your goal '{goal}' is only {new_progress}% done.", user["email"])
#         elif new_progress == 100:
#             send_email(f"✅ Congrats {user['username']}", f"You completed '{goal}'.", user["email"])

#     # Dashboard
#     st.subheader("Your Monthly Progress")
#     fig = px.bar(df_user, x="Month", y="Progress", color="Progress", text="Progress", color_continuous_scale="Blues")
#     st.plotly_chart(fig, use_container_width=True)

#     st.subheader("Goal Details")
#     for _, row in df_user.iterrows():
#         with st.expander(f"Month {row['Month']}: {row['Goal']}"):
#             st.write("Tasks:", row["Tasks"])
#             st.progress(int(row["Progress"]) / 100)


import streamlit as st
import pandas as pd
import plotly.express as px
from automation.email_notifier import send_email
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def show():
    user = st.session_state["user"]
    st.title(f"{user['username'].capitalize()}'s Roadmap")

    df = pd.read_csv("data/roadmap.csv")

    # Admin can view/edit all rows
    if user["role"].lower() == "admin":
        df_user = df.copy()
        st.subheader("Admin: Full Team View")
    else:
        df_user = df[df["Username"] == user["username"]].copy()
        st.subheader("Your Tasks")

    # Editable progress
    selected_month = st.selectbox("Select Month", df_user["Month"])
    current_progress = int(df_user.loc[df_user["Month"] == selected_month, "Progress"].values[0])

    # Admin can edit anyone's progress; team members only their own
    if user["role"].lower() == "admin":
        new_progress = st.slider("Update Progress (%)", 0, 100, current_progress)
    else:
        new_progress = st.slider("Update Progress (%)", 0, 100, current_progress, disabled=False)

    if st.button("Save Progress"):
        df.loc[(df["Month"] == selected_month) & (df["Username"] == df_user.loc[df_user["Month"] == selected_month, "Username"].values[0]), "Progress"] = new_progress
        df.to_csv("data/roadmap.csv", index=False)
        st.success("Progress updated.")

        goal = df_user.loc[df_user["Month"] == selected_month, "Goal"].values[0]
        if new_progress < 50:
            send_email(f"⚠️ Reminder: {user['username']} Low Progress", f"Goal '{goal}' is only {new_progress}% done.", user["email"])
        elif new_progress == 100:
            send_email(f"✅ Congrats {user['username']}", f"You completed '{goal}'.", user["email"])

    # KPI Metrics
    st.subheader("Performance KPIs")
    tasks_completed = df_user[df_user["Progress"] >= 100].shape[0]
    avg_progress = df_user["Progress"].mean()
    st.metric("Tasks Completed", tasks_completed)
    st.metric("Average Progress (%)", round(avg_progress, 2))

    # Progress chart
    fig = px.bar(df_user, x="Month", y="Progress", color="Progress", text="Progress", color_continuous_scale="Blues")
    st.plotly_chart(fig, use_container_width=True)

    # Task details
    st.subheader("Goal Details")
    for _, row in df_user.iterrows():
        with st.expander(f"Month {row['Month']}: {row['Goal']}"):
            st.write("Tasks:", row["Tasks"])
            st.progress(int(row["Progress"]) / 100)

