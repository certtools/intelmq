# SPDX-FileCopyrightText: 2021 Birger Schacht
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from enum import Enum
from termstyle import green
import json


class BotType(str, Enum):
    COLLECTOR   = "Collector"
    PARSER      = "Parser"
    EXPERT      = "Expert"
    OUTPUT      = "Output"

    def toJson(self):
        return self.value


class ReturnType(str, Enum):
    TEXT        = "Text"
    JSON        = "Json"
    PYTHON      = "Python"

    def toJson(self):
        return self.value


MESSAGES = {
    'enabled': 'Bot %s is enabled.',
    'disabled': 'Bot %s is disabled.',
    'starting': 'Starting %s...',
    'running': green('Bot %s is running.'),
    'stopped': 'Bot %s is stopped.',
    'stopping': 'Stopping bot %s...',
    'reloading': 'Reloading bot %s ...',
    'enabling': 'Enabling %s.',
    'disabling': 'Disabling %s.',
    'reloaded': 'Bot %s is reloaded.',
    'restarting': 'Restarting %s...',
}


ERROR_MESSAGES = {
    'starting': 'Bot %s failed to START.',
    'running': 'Bot %s is still running.',
    'stopped': 'Bot %s was NOT RUNNING.',
    'stopping': 'Bot %s failed to STOP.',
    'not found': ('Bot %s FAILED to start because the executable cannot be found. '
                  'Check your PATH variable and your the installation.'),
    'access denied': 'Bot %s failed to %s because of missing permissions.',
    'unknown': 'Status of Bot %s is unknown: %r.',
}


class LogLevel(Enum):
    DEBUG    = 0
    INFO     = 1
    WARNING  = 2
    ERROR    = 3
    CRITICAL = 4
