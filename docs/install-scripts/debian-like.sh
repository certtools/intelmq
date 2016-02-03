#!/usr/bin/env bash

apt-get install python3 python3-pip
apt-get install git build-essential libcurl4-gnutls-dev libffi-dev python-dev
apt-get install redis-server

pip3 install -r REQUIREMENTS
python3 setup.py install

useradd -d /opt/intelmq -U -s /bin/bash intelmq
echo 'export PATH="$PATH:$HOME/bin"' > /opt/intelmq/.profile
chmod -R 0770 /opt/intelmq
chown -R intelmq.intelmq /opt/intelmq
echo 'export INTELMQ_PYTHON=/usr/bin/python3' >> /opt/intelmq/.profile
