import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
from modules.campaign_management import get_campaigns
from modules.analytics import calculate_roi
from modules.reporting import generate_excel_report
import pandas as pd
import plotly.express as px

def show():
    st.subheader("Campaign Dashboard")
    client_id = st.number_input("Client ID", min_value=1, step=1)
    campaigns = get_campaigns(client_id)

    if campaigns:
        df = pd.DataFrame(campaigns, columns=["id","client_id","name","type","budget","start_date","end_date","spend","revenue","status"])
        df['ROI'] = df.apply(lambda row: calculate_roi(row['spend'], row['revenue']), axis=1)
        st.dataframe(df[['name','type','budget','spend','revenue','ROI','status']])

        # ROI Bar Chart
        fig = px.bar(df, x='name', y='ROI', color='ROI', text='ROI', title='ROI by Campaign')
        st.plotly_chart(fig)

        if st.button("Generate Excel Report"):
            path = generate_excel_report(client_id)
            st.success(f"Report generated: {path}")
    else:
        st.info("No campaigns found for this client.")
