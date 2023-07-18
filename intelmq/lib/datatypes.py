# SPDX-FileCopyrightText: 2021 Birger Schacht, 2023 Bundesamt für Sicherheit in der Informationstechnik (BSI)
#
# SPDX-License-Identifier: AGPL-3.0-or-later
from enum import Enum
from inspect import signature
from sys import version_info
from typing import Optional, Callable, Union, List

from datetime import datetime
from termstyle import green
from intelmq.lib.exceptions import InvalidArgument
from intelmq.lib.harmonization import DateTime


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


class TimeFormat(str):
    """
    Pydantic style Field Type class for bot parameter time_format. Used for validation.
    """

    def __new__(cls, value: Optional[str] = None):
        """
        Because str is immutable and we want to manipulate it, it must be done before the object is instantiated.
        Therefore it is necessary to overload __new__ method.
        """
        value = value or "fuzzy"
        return super().__new__(cls, value)

    def __init__(self, value: Optional[str] = None):

        self.convert: Callable
        self.format_string: Optional[str] = None

        super().__init__()

        if isinstance(value, TimeFormat):
            self.convert = value.convert
            self.format_string = value.format_string
        else:
            self.convert, self.format_string = TimeFormat.validate(self)

    def parse_datetime(self, value: str, return_datetime: bool = False) -> Union[datetime, str]:
        """
        This function uses the selected conversion function to parse the datetime value.

        :param value: external datetime string
        :param return_datetime: whether to return string or datetime object
        :return: parsed datetime or string
        """
        if self.format_string:
            return self.convert(value=value, format=self.format_string, return_datetime=return_datetime)
        else:
            return self.convert(value=value, return_datetime=return_datetime)

    @staticmethod
    def validate(value: str) -> [Callable, Optional[str]]:
        """
        This function validates the time_format parameter value.

        :param value: bot parameter for datetime conversion
        :return: correct time conversion function and the format string
        """

        split_value: List[str] = value.split('|')
        conversion: Callable
        conversion_name: str = split_value[0]
        format_string: Optional[str] = split_value[1] if len(split_value) > 1 else None

        # validation of the conversion name
        if conversion_name in DateTime.TIME_CONVERSIONS.keys():
            conversion = DateTime.TIME_CONVERSIONS[conversion_name]

        else:
            raise InvalidArgument(argument="time_format", got=value,
                                  expected=[key for key in DateTime.TIME_CONVERSIONS.keys()])

        # validate that we have format_string when the conversion function expects it
        if not format_string and signature(conversion).parameters.get("format"):
            raise InvalidArgument(argument="time_format", got=value,
                                  expected=f"{conversion_name}|FORMAT_STRING")

        # validate that we do not have format_string when the conversion function doesn't expect it
        elif format_string and not signature(conversion).parameters.get("format"):
            raise InvalidArgument(argument="time_format", got=value,
                                  expected=conversion_name)

        return conversion, format_string


if version_info < (3, 9):
    class Dict39(dict):
        """
        Python 3.9 introduced the handy | operator for dicts.
        For backwards-compatibility, this is the backport
        as IntelMQ supports Python >= 3.7
        """
        def __or__(self, other: dict) -> 'Dict39':
            """
            Create a new dictionary with the merged keys and values of d and other, which must both be dictionaries. The values of other take priority when d and other share keys.
            """
            ret = Dict39(self.copy())
            ret.update(other)
            return ret
else:
    Dict39 = dict
