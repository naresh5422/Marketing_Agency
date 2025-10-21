import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def show_admin_dashboard():
    st.title("📊 Admin Analytics Dashboard")

    df = pd.read_csv("data/roadmap.csv")

    # Summary statistics
    st.subheader("Team Performance Overview")
    team_summary = df.groupby("Username", as_index=False)["Progress"].mean()
    st.dataframe(team_summary)

    # Chart 1: Progress by Team Member
    st.subheader("Average Progress by Team Member")
    fig = px.bar(team_summary, x="Username", y="Progress", color="Progress", text="Progress",
                 color_continuous_scale="Blues", title="Team Progress Comparison")
    st.plotly_chart(fig, use_container_width=True)

    # Chart 2: Monthly Progress Trend
    st.subheader("Progress Trend Across Months")
    fig2 = px.line(df, x="Month", y="Progress", color="Username", markers=True, title="Monthly Progress Trend")
    st.plotly_chart(fig2, use_container_width=True)

    # Chart 3: Task Completion Heatmap
    st.subheader("Team Month-wise Completion Heatmap")
    pivot_df = df.pivot(index="Username", columns="Month", values="Progress")
    fig3 = px.imshow(pivot_df, text_auto=True, color_continuous_scale="Greens", aspect="auto")
    st.plotly_chart(fig3, use_container_width=True)

    # Download section
    st.subheader("Download Reports")

    # Excel
    def to_excel(dataframe):
        buffer = BytesIO()
        dataframe.to_excel(buffer, index=False)
        buffer.seek(0)
        return buffer

    excel_buffer = to_excel(df)
    st.download_button(
        label="⬇️ Download Excel Report",
        data=excel_buffer,
        file_name="marketing_agency_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # PDF
    def generate_pdf(dataframe):
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        pdf.setFont("Helvetica", 12)
        pdf.drawString(30, 750, "Marketing Agency Progress Report")

        y = 720
        for _, row in dataframe.iterrows():
            text = f"Month {row['Month']} | {row['Username']} | {row['Goal']} | {row['Progress']}%"
            pdf.drawString(30, y, text)
            y -= 20
            if y < 50:
                pdf.showPage()
                pdf.setFont("Helvetica", 12)
                y = 750

        pdf.save()
        buffer.seek(0)
        return buffer

    pdf_buffer = generate_pdf(df)
    st.download_button(
        label="⬇️ Download PDF Report",
        data=pdf_buffer,
        file_name="marketing_agency_report.pdf",
        mime="application/pdf"
    )
