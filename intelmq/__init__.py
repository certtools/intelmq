# SPDX-FileCopyrightText: 2014 Tomás Lima
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from .version import __version__, __version_info__  # noqa: F401
import os
import pathlib
import sys


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
HARMONIZATION_CONF_FILE = os.path.join(CONFIG_DIR, "harmonization.conf")
RUNTIME_CONF_FILE = os.path.join(CONFIG_DIR, "runtime.yaml")
old_runtime_conf_file = pathlib.Path(RUNTIME_CONF_FILE).with_suffix('.conf')
if not pathlib.Path(RUNTIME_CONF_FILE).exists() and old_runtime_conf_file.exists():
    old_runtime_conf_file.rename(RUNTIME_CONF_FILE)
STATE_FILE_PATH = os.path.abspath(os.path.join(VAR_STATE_PATH,
                                               '../state.json'))
