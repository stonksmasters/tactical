#!/bin/bash
# update.sh - update dependencies or restart the application

# Example: reinstall dependencies and restart the app
pip install -r requirements.txt
systemctl restart tacticaltracker
