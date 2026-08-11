#!/bin/bash

# App.py variables
export DATABASE_URL='postgresql://cloudoptima_admin:SuperSecureDbPassword123!@127.0.0.1:5432/cloudoptima_db'
export S3_STATE_BUCKET='cloudoptima-tf-state-12345'

# Generator.py variables
export AWS_REGION="eu-north-1"
export VPC_NAME="cloudoptima"
export SUBNET_ID="subnet-05a93b54d68e26b16"
export KEY_NAME="cloudoptima-key"
export TF_STATE_BUCKET="cloudoptima-tf-state-12345"
export SSH_CIDR="10.0.0.0/16"

# Start Flask
nohup ~/cloudoptima/venv/bin/python ~/cloudoptima/backend/app.py > ~/cloudoptima/backend/flask.log 2>&1 &
