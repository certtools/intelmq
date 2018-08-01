from .version import __version__
import os

ROOT_DIR = "/opt/intelmq/"
CONFIG_DIR = os.path.join(ROOT_DIR, "etc/")
DEFAULT_LOGGING_LEVEL = "INFO"
BOTS_FILE = os.path.join(CONFIG_DIR, "BOTS")
DEFAULT_LOGGING_PATH = os.path.join(ROOT_DIR, "var/log/")
DEFAULTS_CONF_FILE = os.path.join(CONFIG_DIR, "defaults.conf")
HARMONIZATION_CONF_FILE = os.path.join(CONFIG_DIR, "harmonization.conf")
PIPELINE_CONF_FILE = os.path.join(CONFIG_DIR, "pipeline.conf")
RUNTIME_CONF_FILE = os.path.join(CONFIG_DIR, "runtime.conf")
VAR_RUN_PATH = os.path.join(ROOT_DIR, "var/run/")
