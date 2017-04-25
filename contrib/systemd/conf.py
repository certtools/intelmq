# -*- coding: utf-8 -*-
import os.path
import shutil

from intelmq import ROOT_DIR

__all__ = ['ACCURACY_SECS', 'DISABLE_IN_CONF', 'ON_ACTIVE_SEC', 'SET_RUNMODE_IN_CONF',
           'INTELMQ_GROUP', 'RANDOMIZE_DELAYS', 'SYSTEMD_OUTPUT_DIR', 'ROOT_DIR', 'SYSTEMCTL_BIN',
           'INTELMQCTL_BIN', 'SERVICE_PREFIX', 'INTELMQ_USER']

ACCURACY_SECS = '100ms'
DISABLE_IN_CONF = True
INTELMQCTL_BIN = shutil.which('intelmqctl')
INTELMQ_GROUP = 'intelmq'
INTELMQ_USER = 'intelmq'
ON_ACTIVE_SEC = '30 minutes'
RANDOMIZE_DELAYS = '45 minutes'
SERVICE_PREFIX = "intelmq."
SET_RUNMODE_IN_CONF = True
SYSTEMCTL_BIN = shutil.which('systemctl')
SYSTEMD_OUTPUT_DIR = os.path.join(ROOT_DIR, 'etc/systemd')
