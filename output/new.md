

This is the `master_README.md` file. This is where you mix your static content with placeholder template variables 

The below template variable **timed_process_killer** will get populated with the contents of `scripts/timed_process_killer.sh`: 
 
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
updateString="'apt-get update', 'apt-get upgrade -y', 'apt-get autoclean' ran | $myDate"
echo $updateString >> ~/Code/AutoUpdates/log/AutoUpdate.log 
apt-get update && apt-get upgrade -y && apt-get autoclean

```


Files with dots (`.`) in their names work, below is `scripts/test.echo.sh`:

```
#!/bin/bash
echo "This script isn't terribly useful."
echo "It demonstrates a file with dots ('.') in it's name"

```


This is static content, but below is a file with dashes in it's name from `scripts/script-with-dashes.py`:

```
#!/usr/bin/env python
from __future__ import print_function
print("I'm a script with dashes in my name")

```

