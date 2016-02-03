#!/usr/bin/env bash

apt-get install python
apt-get install git build-essential libcurl4-gnutls-dev libffi-dev libgnutls28-dev
apt-get install python-dev python-pip python-pycurl python-openssl python-pyasn1
apt-get install redis-server

pip2 install -r REQUIREMENTS2
python2.7 setup.py install

useradd -d /opt/intelmq -U -s /bin/bash intelmq
echo 'export PATH="$PATH:$HOME/bin"' > /opt/intelmq/.profile
chmod -R 0770 /opt/intelmq
chown -R intelmq.intelmq /opt/intelmq
