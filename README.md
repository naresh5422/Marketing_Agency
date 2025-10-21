# Marketing_Agency

This project is a comprehensive dashboard for a marketing agency, built with Streamlit. It serves as a central control center for managing clients, tracking marketing campaign performance, and monitoring internal team progress via an authenticated roadmap tracker.

## Key Features

*   **Client Dashboard**: View a list of all clients and add new ones to the database.
*   **Campaign Dashboard**: Analyze campaign performance for specific clients, calculate ROI, and generate Excel reports.
*   **Roadmap Tracker**: An internal tool for teams to track monthly goals and progress. It includes:
    *   User authentication with distinct roles (Admin, Team Member).
    *   A personalized view for team members to update their task progress.
    *   An admin-only view with full team analytics, charts, and reporting capabilities (Excel/PDF downloads).
*   **Automated Scheduling**: Background jobs for sending weekly progress reminders and monthly summary reports to the admin.

## Project Workflow

1.  **Setup**:
    *   Clone the repository and create a virtual environment.
    *   Install the required dependencies: `pip install -r requirements.txt`.
    *   Create a `.env` file based on `config/env.example` and add your email credentials for the notification system to work.

2.  **Database Initialization**:
    *   Run `python scripts/migrate_db.py` to create the `clients.db` SQLite database and its tables.
    *   Run `python scripts/sample_data_loader.py` to populate the database with sample clients, campaigns, and users for the roadmap.

3.  **Running the Application**:
    *   Launch the Streamlit app by running: `streamlit run app.py`.
    *   The application will open in your web browser.

## Project Structure:

marketing_agency/
│
├── app.py                     # Main Streamlit app entry
├── requirements.txt           # Python dependencies
├── config/
│   ├── config.py              # API keys, DB credentials, global configs
│   └── env.example            # Sample environment variables
│
├── modules/
│   ├── client_management.py   # CRUD operations for clients
│   ├── campaign_management.py # Create/update marketing campaigns
│   ├── analytics.py           # Fetch and calculate KPIs
│   ├── reporting.py           # Generate PDF/Excel reports
│   ├── automation.py          # Email reminders, social media scheduling
│   └── utils.py               # Helper functions
│
├── data/
│   ├── clients.db             # SQLite/PostgreSQL database
│   ├── leads.csv              # Lead information
│   └── campaign_templates/    # Predefined campaign templates
│
├── assets/
│   ├── logo.png
│   └── images/                # Images used in campaigns
│
├── dashboards/
│   ├── client_dashboard.py    # Streamlit pages for clients
│   └── campaign_dashboard.py  # Campaign performance dashboard
│
├── scripts/
│   ├── migrate_db.py          # DB setup & migrations
│   └── sample_data_loader.py  # Load test clients/campaigns
│
└── logs/
    └── app.log                # Logging of app events & errors
