import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.automation import start_scheduled_jobs

if __name__ == "__main__":
    start_scheduled_jobs()
