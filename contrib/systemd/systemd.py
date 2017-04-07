import json
import os.path
import shutil
import datetime
import collections
import pwd
import grp
import os

from string import Template

INTELMQ_DIR = '/opt/intelmq'
RUNTIME_CONF = INTELMQ_DIR+'/etc/runtime.conf'
SYSTEMD_OUTPUT_DIR = INTELMQ_DIR+'/etc/systemd'
SERVICE_PREFIX = "intelmq."
DISABLE_IN_CONF = True
SET_RUNMODE_IN_CONF = True
BOT_TYPE = "Collector"
INTELMQCTL_BIN=shutil.which('intelmqctl')
INTELMQ_USER='intelmq'
INTELMQ_GROUP='intelmq'


service_template = Template('''[Unit]
Description=IntelMQ bot $bot Service Unit
After=network.target
RefuseManualStart=no
RefuseManualStop=no

[Service]
Type=oneshot
ExecStart=$bot_run_cmd
#ExecStartPost=
User=$intelmq_user
Group=$intelmq_group

[Install]
WantedBy=multi-user.target
''')

timer_template = Template('''[Unit]
Description=IntelMQ bot $bot Timer Unit
After=network.target
RefuseManualStart=no
RefuseManualStop=no

[Timer]
Persistent=true
AccuracySec=100ms
RandomizedDelaySec=45minutes
OnActiveSec=25minutes
OnUnitActiveSec=$bot_interval seconds
Unit=$service_file_name

[Install]
WantedBy=multi-user.target
''')

POST_DOCS='''
TO INSTALL
==========
cp intelmq.*.service /etc/systemd/system
cp intelmq.*.timer /etc/systemd/system
chmod 664 /etc/systemd/system/intelmq.*.service
chmod 664 /etc/systemd/system/intelmq.*.timer
systemctl daemon-reload
systemctl start intelmq.*.timer
systemctl enable intelmq.*.timer

TO VIEW
=======
systemctl list-timers --all

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

with open(RUNTIME_CONF, encoding='utf-8') as rc_file:
    rc_data = json.loads(rc_file.read())

if not os.path.exists(SYSTEMD_OUTPUT_DIR):
        os.makedirs(SYSTEMD_OUTPUT_DIR)

intelmq_user=INTELMQ_USER
intelmq_group=INTELMQ_GROUP

for bot in rc_data:
    bot_data = rc_data[bot]
    bot_group = bot_data['group']

    if bot_group == BOT_TYPE:

        if DISABLE_IN_CONF:
           rc_data[bot]['enabled'] = False

        if SET_RUNMODE_IN_CONF:
           rc_data[bot]['run_mode'] = 'scheduled'

        bot_parameters = bot_data['parameters']
        bot_interval = int(bot_parameters['rate_limit']/5)
        bot_run_cmd = INTELMQCTL_BIN+' run '+bot
        service_file_name = SYSTEMD_OUTPUT_DIR+os.path.sep+SERVICE_PREFIX+bot+'.service'
        timer_file_name = SYSTEMD_OUTPUT_DIR+os.path.sep+SERVICE_PREFIX+bot+'.timer'
        service_data = service_template.substitute(locals())
        timer_data = timer_template.substitute(locals())
        with open(service_file_name, "w", encoding='utf-8') as svc_file:
            svc_file.write(service_data)
        with open(timer_file_name, "w", encoding='utf-8') as tmr_file:
            tmr_file.write(timer_data)

if DISABLE_IN_CONF or SET_RUNMODE_IN_CONF:
    shutil.move(RUNTIME_CONF, RUNTIME_CONF+'.bak')
    rc_data = collections.OrderedDict(sorted(rc_data.items()))
    data = json.dumps(rc_data, indent=4)
    with open(RUNTIME_CONF, "w", encoding='utf-8') as rc_file:
        rc_file.write(data)
    intelmq_uid = pwd.getpwnam(intelmq_user).pw_uid
    intelmq_gid = grp.getgrnam(intelmq_group).gr_gid
    os.chown(RUNTIME_CONF, intelmq_uid, intelmq_gid)

print(POST_DOCS)
