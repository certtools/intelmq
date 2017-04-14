from string import Template


SERVICE_TEMPLATE = Template('''[Unit]
Description=IntelMQ bot $bot Service Unit
After=network.target
RefuseManualStart=no
RefuseManualStop=no

[Service]
Type=oneshot
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




POST_DOCS='''
TO INSTALL
==========
cd /opt/intelmq/etc/systemd
cp intelmq.*.service /etc/systemd/system
cp intelmq.*.timer /etc/systemd/system
chmod 664 /etc/systemd/system/intelmq.*.service
chmod 664 /etc/systemd/system/intelmq.*.timer
systemctl daemon-reload
systemctl start intelmq.*.timer
systemctl enable intelmq.*.timer

TO VIEW
=======
systemctl list-timers intelmq.*

TO REMOVE
=========
systemctl stop intelmq.*.service
systemctl stop intelmq.*.timer
systemctl disable intelmq.*.service
systemctl disable intelmq.*.timer
rm /etc/systemd/system/intelmq.*.service
rm /etc/systemd/system/intelmq.*.timer
systemctl daemon-reload
systemctl reset-failed


ON DEBIAN8 GET SYSTEMD-230
==========================
echo "deb http://ftp.debian.org/debian jessie-backports main" >> /etc/apt/sources.list.d/debian-backports.list
apt-get update
apt-get -t jessie-backports install systemd
'''
