import yaml
from chronos_api import chronosAPI, print_pretty

# --- LOAD CHRONOS CONFIGURATION ---
with open("config.yaml", "r") as file:
    chronos_data = yaml.safe_load(file)

# --- CHRONOS INSTANCE ---
try:
    client = chronosAPI(**chronos_data)
except:
    print("Error during the initial connection to {hostname}:{port}")
    exit(1)

# --- SET JOB CONFIGURATION ---
docker_image = "fake-image"
paths_to_mount = ["/path/to/mount"]
nb_path = "/absolute/path/to/notebook.ipynb"
job_name = "job-name"
resources = { "cpus": 4,
              "mem": 4096,
              "disk": 0,
              "gpus": 0}


# --- CREATE JOB TO SUBMIT ---
l_jobs = list()
for i in range(1):
    job_sc = client.create_notebook_job(nb_path,
                                        job_name, 
                                        docker_image, 
                                        paths_to_mount, 
                                        resources)
    print_pretty(job_sc)
    l_jobs.append(job_sc)

# --- SUBMIT JOBS ---
client.send_jobs(l_jobs)