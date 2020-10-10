from .version import __version__, __version_info__  # noqa: F401
import os


path = "opt"
if os.getenv("INTELMQ_ROOT_DIR", False):
    path = "opt"
elif os.getenv('INTELMQ_PATHS_NO_OPT', False):
    path = "lsb"


if path == "lsb":
    ROOT_DIR = os.getenv("ROOT_DIR", "/")
    CONFIG_DIR = os.path.join(ROOT_DIR, "etc/intelmq/")
    DEFAULT_LOGGING_PATH = os.path.join(ROOT_DIR, "var/log/intelmq/")
    VAR_RUN_PATH = os.path.join(ROOT_DIR, "var/run/intelmq/")
    VAR_STATE_PATH = os.path.join(ROOT_DIR, "var/lib/intelmq/bots/")
elif path == "opt":
    ROOT_DIR = os.getenv("INTELMQ_ROOT_DIR", "/opt/intelmq/")
    CONFIG_DIR = os.path.join(ROOT_DIR, "etc/")
    DEFAULT_LOGGING_PATH = os.path.join(ROOT_DIR, "var/log/")
    VAR_RUN_PATH = os.path.join(ROOT_DIR, "var/run/")
    VAR_STATE_PATH = os.path.join(ROOT_DIR, "var/lib/bots/")


DEFAULT_LOGGING_LEVEL = "INFO"
DEFAULTS_CONF_FILE = os.path.join(CONFIG_DIR, "defaults.conf")
HARMONIZATION_CONF_FILE = os.path.join(CONFIG_DIR, "harmonization.conf")
PIPELINE_CONF_FILE = os.path.join(CONFIG_DIR, "pipeline.conf")
RUNTIME_CONF_FILE = os.path.join(CONFIG_DIR, "runtime.conf")
BOTS_FILE = os.path.join(CONFIG_DIR, "BOTS")
STATE_FILE_PATH = path = os.path.abspath(os.path.join(VAR_STATE_PATH,
                                                      '../state.json'))
