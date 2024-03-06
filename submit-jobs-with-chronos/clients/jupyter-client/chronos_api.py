import requests
import simplejson as json
from time import sleep, time
import json 
from datetime import datetime

class chronosAPI:
    def __init__(self, hostname, port, user, password):
        self.hostname = hostname
        self.port = port
        self.auth = (user, password)
        self.base_url = f"http://{self.hostname}:{self.port}"
        self.headers = {'content-type': 'application/json'}
        
    def review_job(self,job_json):
        user = self.auth[0]
        if user not in job_json['name']:
            job_json['name'] = f"{user}-{job_json['name']}"
        job_json["runAsUser"] = user
        job_json["owner"] = user
        job_json["ownerName"] = user
        job_json["schedule"] = "R1//P1Y"
        job_json["container"]['forcePullImage'] = True
        job_json["container"]['type'] = "mesos"
        return job_json
    
    def create_notebook_job(self,nb_path, job_name, docker_image, path_to_mount, resources, papermill_parameters = ""):
        now = datetime.now() # Get the local date and time
        now = f"{now.year}-{now.month}-{now.day}-{now.hour}-{now.minute}-{now.second}-{now.microsecond}"
        nb_dir = '/'.join(nb_path.split('/')[:-1])
        nb_input_name = nb_path.split('/')[-1]
        nb_output_name = nb_input_name.replace(".ipynb",f"_output-{now}.ipynb")
        cmd = f"""cd {nb_dir} && papermill {nb_input_name} {nb_output_name} {papermill_parameters}"""
        container = dict()
        container['image'] = f"{docker_image}"
        container['volumes'] = [{"containerPath": path, "hostPath": path, "mode": "RW"} for path in path_to_mount]
        chronos_json = dict()
        chronos_json["name"] = f"{job_name}-{now}"
        chronos_json["command"] = cmd
        chronos_json["shell"] = True
        chronos_json["retries"] = 4
        chronos_json.update(resources)
        chronos_json["container"] = container
        return chronos_json

    def send_job(self,job_json):
        job_json = self.review_job(job_json)
        job_str = json.dumps(job_json)
        if "schedule" in job_json:
            url = self.base_url + "/v1/scheduler/iso8601"
        else:
            url = self.base_url + "/v1/scheduler/dependency"

        flag = True
        while flag:
            try:
                res = requests.post(url, headers=self.headers, data=job_str,auth=self.auth)
                print(job_json['name'], res)
                flag = False
            except:
                sleep(1)

    def list(self):
        url = self.base_url + "/v1/scheduler/jobs"
        res = requests.get(url, headers=self.headers, auth=self.auth).json()
        return res
    
    def delete(self,job_name):
        url = self.base_url + f"/v1/scheduler/job/{job_name}"
        res = requests.delete(url, headers=self.headers, auth=self.auth)
        if res.status_code == 204:
            print(f"Job '{job_name}' DELETED")
        else:
            print(f"Error during the deleting of job '{job_name}'. Status code: {res.status_code}")
        return res.status_code
            
    def delete_all_jobs(self):
        deleted = 0
        errors = 0
        for job in self.list():
            res = self.delete(job['name'])
            if res == 204:
                deleted += 1
            else:
                errors += 1
        print(f"Deleted {deleted} job(s)")
        if errors > 0:
            print(f"Found {errors} error(s)")
            
            
    def delete_completed_jobs(self):
        deleted = 0
        errors = 0
        for job in self.list():
            if job['successCount'] > 0 :
                res = self.delete(job['name'])
                if res == 204:
                    deleted += 1
                else:
                    errors += 1
        print(f"Deleted {deleted} job(s)")
        if errors > 0:
            print(f"Found {errors} error(s)")
            
    def send_jobs(self, obj):
        print("\nSubmitted Job(s):")
        start_time=time()
        if isinstance(obj, dict):
            l_jobs = 1
            self.send_job(obj)
        elif isinstance(obj, list):
            l_jobs = len(obj)
            for job in obj:
                self.send_job(job)

        print(f"Submitted {l_jobs} job(s) in {time()-start_time:.1f} s")