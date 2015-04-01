This is the `master_README.md` file. 

The below entry will get populated with the contents of `scripts/timed_process_killer.sh`: 
 
```
#!/bin/bash

# This script will find all the PID's of the PROCESS_NAME processes
# that have been running for 10 minutes or more and send each PID a
# SIGKILL.
 
PIDS="`ps ax | egrep "PROCESS_NAME" | grep ":10" | awk '{print $1}'`"
for i in ${PIDS}; do { echo "Killing $i"; kill -9 $i; }; done;
```


Similarly, the entry below this line will get dynamically populated with the contents of `scripts/Auto.sh`:

```
#!/bin/bash
# Runs every day at 4AM, see root crontab
# /var/log/apt/term.log
# /var/log/dpkg.log
myDate=$(date +"%Y-%m-%d | %r")
updateString="'apt-get updatey', 'apt-get upgrade -y', apt-get 'autoclean' ran | $myDate"
echo $updateString >> /home/eha/Code/AutoUpdates/log/AutoUpdate.log 
#echo $updateString
apt-get update 
apt-get upgrade -y
apt-get autoclean
```
