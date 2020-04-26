#!/bin/bash
logfile_path="/var/log/dcp-cron";
dt=$(date '+%d/%m/%Y %H:%M:%S');

# updated IP랑 instance id 보내기
echo "[$dt] Reboot" >> "$logfile_path"

sudo service docker start
echo "[$dt]Docker started" >> "$logfile_path"

