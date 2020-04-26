#!/bin/bash

logfile_path="/var/log/dcp-cron";
# Periodically send ip address with instance id
ip = $(curl https://ipinfo.io/ip);
dt=$(date '+%d/%m/%Y %H:%M:%S');

echo "[$dt] Docker monitor + pulse check" >> "$logfile_path"
