#!/bin/bash
################################################################################
# IntelMQ Installer script for CentOS
#
# NOTES:
#     * Start with a minimal CentOS install and then run this script as root
#     * Tested on CentOS 7
# Usage:
#     sudo sh install-intelmq-centos.sh
#
################################################################################
# VARIABLES

########################################
# Global VARIABLES
########################################
# Do you want to delete the temp files after install (Y/N)
CLEANUP="Y"
# Do you want to use the example configs to get started right away?
# or are you going to use your own configuration files?
USE_EXAMPLES="Y"
# Disable SELinux? if you leave enabled, this will add the needed settings
# recommendedation is to leave SELinux enabled
DISABLE_SELINUX="N"
# All output from the script is appended to this log
SCRIPT=$(basename "$0")
LOG="/tmp/${SCRIPT%.*}.log"
# How about some colour to brighten your day
NC="\e[39m"
RED="\e[31m"
GREEN="\e[32m"
BLUE="\e[34m"
YELLOW="\e[33m"
MAG="\e[95m"

########################################
# Variables for IntelMQ
########################################
# Where to pull IntelMQ from
INTELMQ_REPO="https://github.com/certtools/intelmq.git"
# Where the repo is temporarily placed during install
INTELMQ_TEMP="/tmp/intelmq"
# Where to get pip installer from
PIP_LOC="https://bootstrap.pypa.io/get-pip.py"
# Where to temporarily place the pip installer
PIP_TEMP_LOC="/tmp/get-pip.py"
# The installation location for IntelMQ
INTELMQ_INST="/opt/intelmq"
# Do you intend on making changes to the IntelMQ code?
# Yes I will be = "."
# No I won't = intelmq
REPO_CHOICE="."
#REPO_CHOICE="intelmq"

########################################
# Variables for IntelMQ Manager
########################################
# Do you want to install IntelMQ-Manager (Y/N)
IntelMQ_Manager="Y"
# Where to pull IntelMQ-Manager from
INTELMQ_MAN_REPO="https://github.com/certtools/intelmq-manager.git"
# Where the repo is temporarily placed during install
INTELMQ_MAN_TEMP="/tmp/intelmq-manager"
# The Apache Web location where IntelMQ manager will run from
INTELMQ_MAN_WEB="/var/www"
# What port do you intend to use IntelMQ Manager on?
PORT="80"
# The location of the config.php file
INTELMQ_MAN_PHPCON="$INTELMQ_MAN_WEB/intelmq-manager/php/config.php"

################################################################################
# Functions

function Install_IntelMQ {

  echo -e $RED"Installing IntelMQ"$NC | tee -a $LOG

  echo -e "\n" | tee -a $LOG
  echo -e $GREEN"\t Installing Dependencies, Please Wait....."$NC | tee -a $LOG
  echo -e "\n" >> $LOG

  # Make sure we've updated before starting
  yum -y update 2>&1 >> $LOG

  # Install some handy helper packages
  yum -y install vim deltarpm 2>&1 >> $LOG

  # Install the EPEL Repo in order to get the additional required packages
  # not available in the default repositories
  yum -y install epel-release 2>&1 >> $LOG

  # Install python3
  yum -y install python34 python34-devel 2>&1 >> $LOG

  # Install git and gcc
  yum -y install git libcurl-devel gcc gcc-c++ 2>&1 >> $LOG

  # Install redis
  yum -y install redis 2>&1 >> $LOG

  echo -e "\n" | tee -a $LOG
  echo -e $GREEN"\t Installing PIP"$NC | tee -a $LOG
  echo -e "\n" | tee -a $LOG

  # Download and Install the latest version of pip
  # curl URL --proxy proxyIP:port --proxy-user username:password
  curl "$PIP_LOC" -o "$PIP_TEMP_LOC"
  python3.4 "$PIP_TEMP_LOC" 2>&1 >> $LOG

  # Enable redis on startup and start it now
  systemctl enable redis 2>&1 >> $LOG
  systemctl start redis 2>&1 >> $LOG

  echo -e "\n" | tee -a $LOG
  echo -e $GREEN"\t Installing IntelMQ from repository"$NC | tee -a $LOG
  echo -e "\n" | tee -a $LOG

  # Make sure the directory doesn't exist
  rm -rf "$INTELMQ_TEMP" 2>&1 >> $LOG

  # Clone the current git repository and install
  git clone "$INTELMQ_REPO" "$INTELMQ_TEMP" --progress >> $LOG 2>&1 >> $LOG
  cd "$INTELMQ_TEMP"

  # Install IntelMQ
  # adds share directory to /opt/intelmq
  pip3 install -r REQUIREMENTS 2>&1 >> $LOG
  pip3 install -U $REPO_CHOICE 2>&1 >> $LOG
  # Before the installer runs, set the location where IntelMQ will go
  sed -i "s|install-data=/opt/intelmq|install-data=$INTELMQ_INST|g" setup.cfg
  # adds etc and var to /opt/intelmq
  python3.4 setup.py install 2>&1 >> $LOG
  cd /tmp

  if [[ $USE_EXAMPLES == "Y" ]]
  then
    for conf in "$INTELMQ_INST"/etc/examples/*.conf
    do
      cp $conf "$INTELMQ_INST"/etc/ 2>&1 >> $LOG
    done
  fi

  # Create the intelmq user and set the permissions
  useradd -d "$INTELMQ_INST" -U -s /bin/bash intelmq 2>&1 >> $LOG
  echo 'export PATH="$PATH:$HOME/bin"' >> /opt/intelmq/.profile
  echo 'export INTELMQ_PYTHON=/usr/bin/python3' >> /opt/intelmq/.profile
  chmod -R 0770 "$INTELMQ_INST" 2>&1 >> $LOG
  chown -R intelmq:intelmq "$INTELMQ_INST" 2>&1 >> $LOG

  if [[ $CLEANUP == "Y" ]]
  then
    cd /tmp 2>&1 >> $LOG
    rm -rf "$INTELMQ_TEMP" 2>&1 >> $LOG
    rm -f "$PIP_TEMP_LOC" 2>&1 >> $LOG
  fi

  echo -e "\n" | tee -a $LOG
  echo -e $YELLOW"Finished Installing IntelMQ"$NC | tee -a $LOG

}

function Install_IntelMQ_Manager {

  echo -e "\n" | tee -a $LOG
  echo -e $RED"Installing IntelMQ Manager"$NC | tee -a $LOG
  echo -e "\n" | tee -a $LOG

  # Install the requirements for the web interface
  yum -y install httpd mod_ssl php 2>&1 >> $LOG

  # Allow the ports in the firewall and reload the configuration to apply
  sudo firewall-cmd --permanent --add-port=$PORT/tcp
  sudo firewall-cmd --reload

  # Make sure the dest dir doesn't exist
  rm -rf "$INTELMQ_MAN_TEMP" 2>&1 >> $LOG

  # Clone the repo to a temp dir
  git clone "$INTELMQ_MAN_REPO" "$INTELMQ_MAN_TEMP" --progress >> $LOG 2>&1 >> $LOG
  cp -R "$INTELMQ_MAN_TEMP/intelmq-manager" "$INTELMQ_MAN_WEB/intelmq-manager" 2>&1 >> $LOG
  chown -R apache:apache "$INTELMQ_MAN_WEB/intelmq-manager" 2>&1 >> $LOG

  # add the apache user to the intelmq group.
  usermod -a -G intelmq apache 2>&1 >> $LOG

  # Fix /etc/sudoers
  sed -i 's|Defaults    requiretty|Defaults    !requiretty|g' /etc/sudoers

  # Give the apache user permissions to execute commands as the IntelMQ user
  echo "# Give the apache user permissions to execute commands as IntelMQ" >> /etc/sudoers.d/intelmq
  echo "apache ALL=(intelmq) NOPASSWD: /usr/bin/intelmqctl" >> /etc/sudoers.d/intelmq
  chmod 0440 /etc/sudoers.d/intelmq 2>&1 >> $LOG

  if [[ $DISABLE_SELINUX == "Y" ]]
  then

    echo $RED"Taking the easy way out hey? I'm sure there's a pill for that"$NC
    echo -e "\n"

    # Set SELINUX to disabled
    sed -i 's|SELINUX=enforcing|SELINUX=disabled|g' /etc/selinux/config

  else

    # Set the SELinux exceptions to allow Apache to
    # work properly with IntelMQ Manager

    # Install the Audit2Allow and Audit2Why so we can get IntelMQ working with SELinux
    # these tools are very helpful with SELinux
    yum -y install policycoreutils-python 2>&1 >> $LOG

    # tail -f /var/log/secure
    # Since SELinux is enabled we need to allow httpd to write to certain directories
    chcon -R -t httpd_sys_content_rw_t /opt/intelmq/var 2>&1 >> $LOG
    chcon -R -t httpd_sys_content_rw_t /var/www/intelmq-manager/php 2>&1 >> $LOG

    # Allow httpd mod auth
    setsebool -P allow_httpd_mod_auth_pam 1 2>&1 >> $LOG

    # Allow httpd to connect to the redis server over tcp/ip
    setsebool -P httpd_can_network_connect on 2>&1 >> $LOG

    # Allow httpd to run stickshift
    setsebool -P httpd_run_stickshift 1 2>&1 >> $LOG

    # Allow httpd to setrlimit
    setsebool -P httpd_setrlimit 1 2>&1 >> $LOG

    # Allow httpd to read user content
    setsebool -P httpd_read_user_content 1

  fi

  # change the path for the Controller variable in config.php
  sed -i 's|$CONTROLLER = "sudo -u intelmq /usr/local/bin/intelmqctl %s";|$CONTROLLER = "sudo -u intelmq /usr/bin/intelmqctl %s";|g' "$INTELMQ_MAN_PHPCON"

  # change apache to listen on the required port
  sed -i "s|Listen 80|Listen $PORT|g" /etc/httpd/conf/httpd.conf
  # change the root to be intelmq
  sed -i 's|DocumentRoot "/var/www/html"|DocumentRoot "/var/www/intelmq-manager"|g' /etc/httpd/conf/httpd.conf

  # Set apache to start on boot, and start it up
  systemctl enable httpd 2>&1 >> $LOG
  systemctl start httpd 2>&1 >> $LOG

  if [[ $CLEANUP == "Y" ]]
  then
    cd /tmp
    rm -rf "$INTELMQ_MAN_TEMP"
  fi

  echo -e "\n"
  echo -e $YELLOW"Finished Installing IntelMQ Manager"$NC

}

################################################################################

# Clear screen and fresh log
clear
echo "" > $LOG
cd /tmp 2>&1 >> $LOG

echo -e "\n" | tee -a $LOG
echo -e $MAG"Installation script started `date`"$NC | tee -a $LOG
echo -e "\n" | tee -a $LOG

# Install IntelMQ
Install_IntelMQ

# Install the manager if requested
if [[ $IntelMQ_Manager == "Y" ]]
then
  Install_IntelMQ_Manager
fi

echo -e "\n" | tee -a $LOG
echo -e $MAG"Installation script finished `date`"$NC | tee -a $LOG
echo -e "\n" | tee -a $LOG

################################################################################
