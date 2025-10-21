import os

DB_PATH = os.getenv("DB_PATH", "data/clients.db")
LOG_FILE = os.getenv("LOG_FILE", "logs/app.log")
SYSTEM_PATH = "sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))"
