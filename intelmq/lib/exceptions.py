# SPDX-FileCopyrightText: 2015 Dognaedis
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
    IntelMQ Exception Class
"""
from typing import Any, Optional, Union

__all__ = ['InvalidArgument', 'ConfigurationError', 'IntelMQException',
           'IntelMQHarmonizationException', 'InvalidKey', 'InvalidValue',
           'KeyExists', 'KeyNotExists', 'PipelineError',
           'MissingDependencyError',
           ]


class IntelMQException(Exception):

    def __init__(self, message):
        super().__init__(message)


"""
    IntelMQ Exception SubClasses
"""


class InvalidArgument(IntelMQException):

    def __init__(self, argument: Any, got: Any = None, expected=None,
                 docs: str = None):
        message = f"Argument {repr(argument)} is invalid."
        if expected is list:
            message += f" Should be one of: {list}."
        elif expected:  # not None
            message += f" Should be of type: {expected}."
        if got:
            message += f" Got {repr(got)}."
        if docs:
            message += f" For more information see {docs}"
        super().__init__(message)


class PipelineError(IntelMQException):

    def __init__(self, argument: Union[str, Exception]):
        message = f"pipeline failed - {repr(argument)}"
        super().__init__(message)


class ConfigurationError(IntelMQException):

    def __init__(self, config: str, argument: str):
        message = f"{config} configuration failed - {argument}"
        super().__init__(message)


class PipelineFactoryError(IntelMQException):
    pass


"""
    IntelMQ Harmonization Exception Class
"""


class IntelMQHarmonizationException(IntelMQException):

    def __init__(self, message):
        super().__init__(message)


"""
    IntelMQ Harmonization Exception sub classes
"""


class InvalidValue(IntelMQHarmonizationException):

    def __init__(self, key: str, value: str, reason: Any = None, object: bytes = None):
        message = (f"invalid value {value!r} ({type(value)}) for key {key!r}{': ' + reason if reason else ''}")
        self.object = object
        super().__init__(message)


class InvalidKey(IntelMQHarmonizationException, KeyError):

    def __init__(self, key: str):
        message = f"invalid key {repr(key)}"
        super().__init__(message)


class KeyExists(IntelMQHarmonizationException):

    def __init__(self, key: str):
        message = f"key {repr(key)} already exists"
        super().__init__(message)


class KeyNotExists(IntelMQHarmonizationException):

    def __init__(self, key: str):
        message = f"key {repr(key)} not exists"
        super().__init__(message)


class MissingDependencyError(IntelMQException):
    """
    A missing dependency was detected. Log instructions on installation.
    """
    def __init__(self, dependency: str, version: Optional[str] = None,
                 installed: Optional[str] = None,
                 additional_text: Optional[str] = None):
        """
        Parameters:
            dependency (str): The dependency name.
            version (Optional[str], optional): The required version. The default is None.
            installed (Optional[str], optional)
                The currently installed version. Requires 'version' to be given The default is None.
            additional_text (Optional[str], optional):
                Arbitrary additional text to show. The default is None.

        Returns:
            IntelMQException: with prepared text
        """
        appendix = ""
        if version:
            higher = " or higher" if not any(x in version for x in '<>=') else ""
            appendix = (f" Please note that this bot requires {dependency} version {version}{higher}!")
            if installed:
                if isinstance(installed, tuple):
                    installed = ".".join(map(str, installed))
                appendix = appendix + (f" Installed is version {installed!r}.")
        if additional_text:
            appendix = f"{appendix} {additional_text}"
        message = (f"Could not load dependency {dependency!r}, please install it "
                   "with apt/yum/dnf/zypper (possibly named "
                   f"python3-{dependency}) or pip3.{appendix}")
        super().__init__(message)


class DecodingError(IntelMQException, ValueError):
    """
    This is a separate Error to distinguish it from other exceptions as it is
    unrecoverable.
    """
    def __init__(self, encodings=None, exception: UnicodeDecodeError = None,
                 object: bytes = None):
        self.object = object
        suffixes = []
        if encodings:
            suffixes.append(f"with given encodings {encodings}")
        if exception:
            suffixes.append(f'at position {exception.start} with length {exception.end} ({exception.object[exception.start:exception.end]})')
            suffixes.append(f'with reason {exception.reason}')
        suffix = (' ' + ' '.join(suffixes)) if suffixes else ''
        super().__init__(f"Could not decode string{suffix}.")
