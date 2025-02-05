#!/bin/bash
# deploy.sh - deploy updates to the Raspberry Pi

# Example: SSH into the Raspberry Pi and pull the latest changes
ssh pi@<raspi_ip> "cd ~/tactical-signal-tracker && git pull && systemctl restart tacticaltracker"
