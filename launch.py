# ###########################################################################
#
#  CLOUDERA APPLIED MACHINE LEARNING PROTOTYPE (AMP)
#  (C) Cloudera, Inc. 2020
#  All rights reserved.
#
#  Applicable Open Source License: Apache 2.0
#
#  NOTE: Cloudera open source products are modular software products 
#  made up of hundreds of individual components, each of which was 
#  individually copyrighted.  Each Cloudera open source product is a 
#  collective work under U.S. Copyright Law. Your license to use the 
#  collective work is as provided in your written agreement with  
#  Cloudera.  Used apart from the collective work, this file is 
#  licensed for your use pursuant to the open source license 
#  identified above.
#
#  This code is provided to you pursuant a written agreement with
#  (i) Cloudera, Inc. or (ii) a third-party authorized to distribute 
#  this code. If you do not have a written agreement with Cloudera nor 
#  with an authorized and properly licensed third party, you do not 
#  have any rights to access nor to use this code.
#
#  Absent a written agreement with Cloudera, Inc. (“Cloudera”) to the
#  contrary, A) CLOUDERA PROVIDES THIS CODE TO YOU WITHOUT WARRANTIES OF ANY
#  KIND; (B) CLOUDERA DISCLAIMS ANY AND ALL EXPRESS AND IMPLIED 
#  WARRANTIES WITH RESPECT TO THIS CODE, INCLUDING BUT NOT LIMITED TO 
#  IMPLIED WARRANTIES OF TITLE, NON-INFRINGEMENT, MERCHANTABILITY AND 
#  FITNESS FOR A PARTICULAR PURPOSE; (C) CLOUDERA IS NOT LIABLE TO YOU, 
#  AND WILL NOT DEFEND, INDEMNIFY, NOR HOLD YOU HARMLESS FOR ANY CLAIMS 
#  ARISING FROM OR RELATED TO THE CODE; AND (D)WITH RESPECT TO YOUR EXERCISE 
#  OF ANY RIGHTS GRANTED TO YOU FOR THE CODE, CLOUDERA IS NOT LIABLE FOR ANY
#  DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, PUNITIVE OR
#  CONSEQUENTIAL DAMAGES INCLUDING, BUT NOT LIMITED TO, DAMAGES 
#  RELATED TO LOST REVENUE, LOST PROFITS, LOSS OF INCOME, LOSS OF 
#  BUSINESS ADVANTAGE OR UNAVAILABILITY, OR LOSS OR CORRUPTION OF
#  DATA.
#
# ###########################################################################

!pip3 install --upgrade pip
!pip3  install -q -r requirements.txt
from IPython.display import Javascript, HTML
import os
import time
import datetime
from cmlbootstrap import CMLBootstrap
import numpy as np


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
