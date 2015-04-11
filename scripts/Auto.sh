#!/bin/bash
# Runs every day at 4AM, see root crontab
# /var/log/apt/term.log
# /var/log/dpkg.log
myDate=$(date +"%Y-%m-%d | %r")
updateString="'apt-get update', 'apt-get upgrade -y', 'apt-get autoclean' ran | $myDate"
echo $updateString >> ~/Code/AutoUpdates/log/AutoUpdate.log 
apt-get update && apt-get upgrade -y && apt-get autoclean
