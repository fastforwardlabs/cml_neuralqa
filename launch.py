#
# @license
# Copyright 2020 Cloudera Fast Forward. https://github.com/fastforwardlabs
# Licensed under the MIT License (the "License");
# =============================================================================
#

import numpy as np
from cmlbootstrap import CMLBootstrap
import datetime
import time
import os
from IPython.display import Javascript, HTML


!pip3  install -q -r requirements.txt

run_time_suffix = datetime.datetime.now()
run_time_suffix = run_time_suffix.strftime("%d%m%Y%H%M%S")


HOST = os.getenv("CDSW_API_URL").split(
    ":")[0] + "://" + os.getenv("CDSW_DOMAIN")
USERNAME = os.getenv("CDSW_PROJECT_URL").split("/")[6]
API_KEY = os.getenv("CDSW_API_KEY")
PROJECT_NAME = os.getenv("CDSW_PROJECT")


cml = CMLBootstrap(HOST, USERNAME, API_KEY, PROJECT_NAME)


# Get User Details
user_details = cml.get_user({})
user_obj = {"id": user_details["id"], "username": USERNAME,
            "name": user_details["name"],
            "type": user_details["type"],
            "html_url": user_details["html_url"],
            "url": user_details["url"]
            }


# Get Project Details
project_details = cml.get_project({})
project_id = project_details["id"]


# Create model build script
cdsw_script = """#!/bin/bash
pip3 install -r requirements.txt"""

with open("cdsw-build.sh", 'w+') as f:
    f.write(cdsw_script)
    f.close()
os.chmod("cdsw-build.sh", 0o777)

# Get Default Engine Details
# Engine id is required for next step (create model)

default_engine_details = cml.get_default_engine({})
default_engine_image_id = default_engine_details["id"]


# Create Application
create_application_params = {
    "name": "NeuralQA: Question Answering ",
    "subdomain": run_time_suffix[:],
    "description": "NeuralQA: A Usable Library for Question Answering on Large Datasets with BERT",
    "type": "manual",
    "script": "app.py", "environment": {},
    "kernel": "python3", "cpu": 1, "memory": 4,
    "nvidia_gpu": 0
}

new_application_details = cml.create_application(create_application_params)
application_url = new_application_details["url"]
application_id = new_application_details["id"]

# print("Application may need a few minutes to finish deploying. Open link below in about a minute ..")
print("Application created, deploying at ", application_url)

# Wait for the application to deploy.
is_deployed = False
while is_deployed == False:
    # Wait for the application to deploy.
    app = cml.get_application(str(application_id), {})
    if app["status"] == 'running':
        print("Application is deployed")
        break
    else:
        print("Application deployment status .....", app["status"])
        time.sleep(10)

HTML("<a href='{}'>Open Application UI</a>".format(application_url))
