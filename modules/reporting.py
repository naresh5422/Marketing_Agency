#Export campaign analytics to PDF/Excel
#Use pandas + openpyxl or reportlab
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
from modules.campaign_management import get_campaigns

def generate_excel_report(client_id):
    campaigns = get_campaigns(client_id)
    df = pd.DataFrame(campaigns)
    if df.empty:
        return None # Indicate that no report was generated due to no data
    df.to_excel(f"data/client_{client_id}_report.xlsx", index=False)
    return f"data/client_{client_id}_report.xlsx"


def generate_pdf_report(client_id):
    pass