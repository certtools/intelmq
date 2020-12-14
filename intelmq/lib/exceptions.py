# -*- coding: utf-8 -*-
'''
    IntelMQ Exception Class
'''
from typing import Any, Optional, Union

__all__ = ['InvalidArgument', 'ConfigurationError', 'IntelMQException',
           'IntelMQHarmonizationException', 'InvalidKey', 'InvalidValue',
           'KeyExists', 'KeyNotExists', 'PipelineError',
           'MissingDependencyError',
           ]


class IntelMQException(Exception):

    def __init__(self, message):
        super().__init__(message)


'''
    IntelMQ Exception SubClasses
'''


class InvalidArgument(IntelMQException):

    def __init__(self, argument: Any, got: Any = None, expected=None,
                 docs: str = None):
        message = "Argument {} is invalid.".format(repr(argument))
        if expected is list:
            message += " Should be one of: {}.".format(list)
        elif expected:  # not None
            message += " Should be of type: {}.".format(expected)
        if got:
            message += " Got {}.".format(repr(got))
        if docs:
            message += " For more information see {}".format(docs)
        super().__init__(message)


class PipelineError(IntelMQException):

    def __init__(self, argument: Union[str, Exception]):
        message = "pipeline failed - %s" % repr(argument)
        super().__init__(message)


class ConfigurationError(IntelMQException):

    def __init__(self, config: str, argument: str):
        message = "%s configuration failed - %s" % (config, argument)
        super().__init__(message)


class PipelineFactoryError(IntelMQException):
    pass


'''
    IntelMQ Harmonization Exception Class
'''


class IntelMQHarmonizationException(IntelMQException):

    def __init__(self, message):
        super().__init__(message)


'''
    IntelMQ Harmonization Exception sub classes
'''


class InvalidValue(IntelMQHarmonizationException):

    def __init__(self, key: str, value: str, reason: Any = None):
        message = ("invalid value {value!r} ({type}) for key {key!r}{reason}"
                   "".format(value=value, type=type(value), key=key,
                             reason=': ' + reason if reason else ''))
        super().__init__(message)


class InvalidKey(IntelMQHarmonizationException, KeyError):

    def __init__(self, key: str):
        message = "invalid key %s" % repr(key)
        super().__init__(message)


class KeyExists(IntelMQHarmonizationException):

    def __init__(self, key: str):
        message = "key %s already exists" % repr(key)
        super().__init__(message)


class KeyNotExists(IntelMQHarmonizationException):

    def __init__(self, key: str):
        message = "key %s not exists" % repr(key)
        super().__init__(message)


class MissingDependencyError(IntelMQException):
    """
    A missing dependency was detected. Log instructions on installation.
    """
    def __init__(self, dependency: str, version: Optional[str] = None,
                 installed: Optional[str] = None,
                 additional_text: Optional[str] = None):
        """
        Parameters
        ----------
        dependency : str
            The dependency name.
        version : Optional[str], optional
            The required version. The default is None.
        installed : Optional[str], optional
            The currently installed version. Requires 'version' to be given The default is None.
        additional_text : Optional[str], optional
            Arbitrary additional text to show. The default is None.

        Returns
        -------
        IntelMQException: with prepared text

        """
        appendix = ""
        if version:
            higher = " or higher" if not any(x in version for x in '<>=') else ""
            appendix = (" Please note that this bot requires "
                        "{dependency} version {version}{higher}!"
                        "".format(dependency=dependency,
                                  version=version,
                                  higher=higher))
            if installed:
                if isinstance(installed, tuple):
                    installed = ".".join(map(str, installed))
                appendix = appendix + (" Installed is version {installed!r}."
                                       "".format(installed=installed))
        if additional_text:
            appendix = "%s %s" % (appendix, additional_text)
        message = ("Could not load dependency {dependency!r}, please install it "
                   "with apt/yum/dnf/zypper (possibly named "
                   "python3-{dependency}) or pip3.{appendix}"
                   "".format(dependency=dependency,
                             appendix=appendix))
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
            suffixes.append("with given encodings %r" % encodings)
        if exception:
            suffixes.append('at position %s with length %d (%r)'
                            '' % (exception.start, exception.end,
                                  exception.object[exception.start:exception.end]))
            suffixes.append('with reason %r' % exception.reason)
        suffix = (' ' + ' '.join(suffixes)) if suffixes else ''
        super().__init__("Could not decode string%s." % suffix)
