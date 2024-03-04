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

# --- COLLECT AND SHOW JOB LIST ---
import pandas as pd
try:
    retrieved_job_list = client.list()
    if len(retrieved_job_list) > 0:
        df = pd.DataFrame.from_records(retrieved_job_list)[["name","successCount","errorCount","lastSuccess","lastError","cpus","mem","gpus","retries"]]
        print(df)
    else:
        print("No job to list")
except:
    print("Error during the command execution")
    exit(1)