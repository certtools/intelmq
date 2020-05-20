# -*- coding: utf-8 -*-
'''
    IntelMQ Exception Class
'''
import traceback

__all__ = ['InvalidArgument', 'ConfigurationError', 'IntelMQException',
           'IntelMQHarmonizationException', 'InvalidKey', 'InvalidValue',
           'KeyExists', 'KeyNotExists', 'PipelineError',
           ]


class IntelMQException(Exception):

    def __init__(self, message):
        super().__init__(message)


'''
    IntelMQ Exception SubClasses
'''


class InvalidArgument(IntelMQException):

    def __init__(self, argument, got=None, expected=None, docs=None):
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

    def __init__(self, argument: Exception):
        if type(argument) is type and issubclass(argument, Exception):
            message = "pipeline failed - %s" % traceback.format_exc(argument)
        else:
            message = "pipeline failed - %s" % repr(argument)
        super().__init__(message)


class ConfigurationError(IntelMQException):

    def __init__(self, config, argument):
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

    def __init__(self, key, value, reason=None):
        message = ("invalid value {value!r} ({type}) for key {key!r}{reason}"
                   "".format(value=value, type=type(value), key=key,
                             reason=': ' + reason if reason else ''))
        super().__init__(message)


class InvalidKey(IntelMQHarmonizationException, KeyError):

    def __init__(self, key):
        message = "invalid key %s" % repr(key)
        super().__init__(message)


class KeyExists(IntelMQHarmonizationException):

    def __init__(self, key):
        message = "key %s already exists" % repr(key)
        super().__init__(message)


class KeyNotExists(IntelMQHarmonizationException):

    def __init__(self, key):
        message = "key %s not exists" % repr(key)
        super().__init__(message)


class DecodingError(IntelMQException, ValueError):
    """
    This is a separate Error to distinguish it from other exceptions as it is
    unrecoverable.
    """
    def __init__(self, encodings=None, exception: UnicodeDecodeError = None,
                 object: bytes = None):
        self.object = object
        suffix = []
        if encodings:
            suffix.append("with given encodings %r" % encodings)
        if exception:
            suffix.append('at position %s with length %d (%r)'
                          '' % (exception.start, exception.end,
                                exception.object[exception.start:exception.end]))
            suffix.append('with reason %r' % exception.reason)
        suffix = (' ' + ' '.join(suffix)) if suffix else ''
        super().__init__("Could not decode string%s." % suffix)
