import shutil
import intelmq

INTELMQ_DIR = '/opt/intelmq'
#RUNTIME_CONF = INTELMQ_DIR+'/etc/runtime.conf'
#PIPELINE_CONF = INTELMQ_DIR+'/etc/pipeline.conf'
RUNTIME_CONF = intelmq.RUNTIME_CONF_FILE
PIPELINE_CONF = intelmq.PIPELINE_CONF_FILE
IGNORED_IDS_FILE = './ignored_ids.txt'
SYSTEMD_OUTPUT_DIR = INTELMQ_DIR+'/etc/systemd'
SERVICE_PREFIX = "intelmq."
DISABLE_IN_CONF = True
SET_RUNMODE_IN_CONF = True
INTELMQCTL_BIN = shutil.which('intelmqctl')
SYSTEMCTL_BIN = shutil.which('systemctl')
INTELMQ_USER = 'intelmq'
INTELMQ_GROUP = 'intelmq'
ACCURACY_SECS = '100ms'
RANDOMIZE_DELAYS = '45 minutes'
ON_ACTIVE_SEC = '30 minutes'
