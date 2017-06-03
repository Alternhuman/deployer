#!/bin/bash
source /var/lib/jenkins/workspace/deployer/monitor/env/bin/activate
python /var/lib/jenkins/workspace/deployer/monitor/app.py --port=$1
