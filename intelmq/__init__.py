from .version import __version__
import os

ROOT_DIR = "/opt/intelmq/"
CONFIG_DIR = os.path.join(ROOT_DIR, "etc/")
DEFAULT_LOGGING_LEVEL = "INFO"
DEFAULT_LOGGING_PATH = os.path.join(ROOT_DIR, "var/log/")
DEFAULTS_CONF_FILE = os.path.join(CONFIG_DIR, "defaults.conf")
HARMONIZATION_CONF_FILE = os.path.join(CONFIG_DIR, "harmonization.conf")
PIPELINE_CONF_FILE = os.path.join(CONFIG_DIR, "pipeline.conf")
RUNTIME_CONF_FILE = os.path.join(CONFIG_DIR, "runtime.conf")
STARTUP_CONF_FILE = os.path.join(CONFIG_DIR, "startup.conf")
SYSTEM_CONF_FILE = os.path.join(CONFIG_DIR, "system.conf")
VAR_RUN_PATH = os.path.join(ROOT_DIR, "var/run/")
