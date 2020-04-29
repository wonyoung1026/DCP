#!/bin/bash
sudo yum update -y

# Timezone setup
sudo yum install -y ntp
sudo ntpdate stdtime.gov.hk
sudo timedatectl set-timezone UTC
#Install pciutils
sudo yum install pciutils

# Check if NVIDIA driver (NVIDIA-SMI) has been installed
# pkg="nvidia-smi";
# if rpm -q $pkg
# then 
#     echo "$pkg installed"
# else
#     echo "$pkg NOT installed"; exit 1;
# fi


# Install python
sudo yum install -y python3
sudo yum install -y epel-release
sudo yum install -y python-pip
sudo yum install -y python-devel

# glances set up for monitoring
sudo yum install -y glances

# DCP related variables
DCP_USER="centos"
DCP_SCRIPT_PATH="/home/$DCP_USER/scripts"


# Add new user (dcp) with sudoer privilage
# For use when there are multiple types of OSes 
# DCP_USER="dcp"
# DCP_SCRIPT_PATH="/home/$DCP_USER/scripts"

# if ! id -u "$DCP_USER"
# then
#     sudo adduser $DCP_USER

#     SUDOER_PATH="/etc/sudoers"
#     sudo chmod 750 "$SUDOER_PATH"
#     sudo cat "$DCP_SCRIPT_PATH/sudoers" > "$SUDOER_PATH"
#     sudo chmod 440 "$SUDOER_PATH"

#     sudo su "$DCP_USER"
#     sudo usermod -aG wheel "$DCP_USER"
# fi




# Remove old and install docker
sudo yum remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-engine
sudo yum install -y yum-utils device-mapper-persistent-data lvm2
sudo yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install docker-ce docker-ce-cli containerd.io -y
sudo systemctl start docker
sudo systemctl enable docker

# User docker without sudo
sudo groupadd docker
sudo usermod -aG docker $(whoami)
sudo service docker restart

# get centos:7 image (More to be added in the future)
# sudo docker pull wonyoung1026/dcp-base-centos


# Create log file for DCP cron jobs 
LOGFILE_PATH="/var/log/dcp-cron";
sudo touch "$LOGFILE_PATH"
dt=$(date '+%d/%m/%Y %H:%M:%S');
echo "[$dt]DCP Log file created" >> "$LOGFILE_PATH"


# Schedule a cron to execute health script every 5 min
# Schedule a cron to execute script on reboot
HEALTH_SCRIPT_CRON ='*/5 * * * * $DCP_USER $DCP_SCRIPT_PATH/health.sh';
REBOOT_SCRIPT_CRON = '@reboot $DCP_USER $DCP_SCRIPT_PATH/reboot.sh'

CRONTAB_PATH = "/etc/crontab";
sudo chmod 750 "$CRONTAB_PATH"
sudo echo "$HEALTH_SCRIPT_CRON" >> "$CRONTAB_PATH"
sudo echo "$REBOOT_SCRIPT_CRON" >> "$CRONTAB_PATH"
sudo chmod 600 "$CRONTAB_PATH"

#restart crond
sudo service crond restart
