from .version import __version__
import os

if os.getenv('INTELMQ_PATHS_NO_OPT', False):
    CONFIG_DIR = "/etc/intelmq/"
    DEFAULT_LOGGING_LEVEL = "INFO"
    BOTS_FILE = os.path.join(CONFIG_DIR, "BOTS")
    DEFAULT_LOGGING_PATH = "/var/log/intelmq/"
    DEFAULTS_CONF_FILE = os.path.join(CONFIG_DIR, "defaults.conf")
    HARMONIZATION_CONF_FILE = os.path.join(CONFIG_DIR, "harmonization.conf")
    PIPELINE_CONF_FILE = os.path.join(CONFIG_DIR, "pipeline.conf")
    RUNTIME_CONF_FILE = os.path.join(CONFIG_DIR, "runtime.conf")
    VAR_RUN_PATH = "/var/run/intelmq/"
    VAR_STATE_PATH = "/var/lib/intelmq/bots/"
else:
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
    VAR_STATE_PATH = os.path.join(ROOT_DIR, "var/lib/bots/")
