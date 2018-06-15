# -*- coding: utf-8 -*-
from string import Template

__all__ = ['TIMER_TEMPLATE', 'SERVICE_TEMPLATE', 'POST_DOCS']


SERVICE_TEMPLATE = Template('''[Unit]
Description=IntelMQ bot $bot Service Unit
After=network.target
RefuseManualStart=no
RefuseManualStop=no

[Service]
Type=$type
ExecStart=$bot_run_cmd
User=$INTELMQ_USER
Group=$INTELMQ_GROUP

[Install]
WantedBy=multi-user.target
''')


TIMER_TEMPLATE = Template('''[Unit]
Description=IntelMQ bot $bot Timer Unit
After=network.target
RefuseManualStart=no
RefuseManualStop=no

[Timer]
Persistent=true
AccuracySec=$ACCURACY_SECS
RandomizedDelaySec=$RANDOMIZE_DELAYS
OnActiveSec=$ON_ACTIVE_SEC
OnUnitActiveSec=$bot_interval seconds
Unit=$bot_service_name

[Install]
WantedBy=multi-user.target
''')


POST_DOCS = '''
TO INSTALL
==========
cd /opt/intelmq/etc/systemd
sudo cp intelmq.*.service /etc/systemd/system
sudo cp intelmq.*.timer /etc/systemd/system
sudo chmod 664 /etc/systemd/system/intelmq.*.service
sudo chmod 664 /etc/systemd/system/intelmq.*.timer
sudo systemctl daemon-reload
sudo systemctl start intelmq.*.timer
sudo systemctl enable intelmq.*.timer

TO VIEW
=======
sudo systemctl list-timers intelmq.*

TO REMOVE
=========
sudo systemctl stop intelmq.*.service
sudo systemctl stop intelmq.*.timer
sudo systemctl disable intelmq.*.service
sudo systemctl disable intelmq.*.timer
sudo rm /etc/systemd/system/intelmq.*.service
sudo rm /etc/systemd/system/intelmq.*.timer
sudo systemctl daemon-reload
sudo systemctl reset-failed


ON DEBIAN8 GET SYSTEMD-230
==========================
echo "deb http://ftp.debian.org/debian jessie-backports main" >> /etc/apt/sources.list.d/debian-backports.list
apt-get update
apt-get -t jessie-backports install systemd
'''
