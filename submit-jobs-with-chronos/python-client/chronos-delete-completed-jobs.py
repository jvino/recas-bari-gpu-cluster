import yaml
from chronos_api import chronosAPI

# --- LOAD CHRONOS CONFIGURATION ---
with open("config.yaml", "r") as file:
    chronos_data = yaml.safe_load(file)

# --- CHRONOS INSTANCE ---
try:
    client = chronosAPI(**chronos_data)
except:
    print("Error during the initial connection to {hostname}:{port}")
    exit(1)

# --- DELETE COMPLETED JOBS ---
try:
    client.delete_completed_jobs()
except:
    print("Error during the command execution")
    exit(1)