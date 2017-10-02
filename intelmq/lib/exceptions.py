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
        super(IntelMQException, self).__init__(message)


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
        super(InvalidArgument, self).__init__(message)


class PipelineError(IntelMQException):

    def __init__(self, argument):
        if type(argument) is type and issubclass(argument, Exception):
            message = "pipeline failed - %s" % traceback.format_exc(argument)
        else:
            message = "pipeline failed - %s" % repr(argument)
        super(PipelineError, self).__init__(message)


class ConfigurationError(IntelMQException):

    def __init__(self, config, argument):
        message = "%s configuration failed - %s" % (config, argument)
        super(ConfigurationError, self).__init__(message)


class PipelineFactoryError(IntelMQException):
    pass


'''
    IntelMQ Harmonization Exception Class
'''


class IntelMQHarmonizationException(IntelMQException):

    def __init__(self, message):
        super(IntelMQHarmonizationException, self).__init__(message)


'''
    IntelMQ Harmonization Exception sub classes
'''


class InvalidValue(IntelMQHarmonizationException):

    def __init__(self, key, value, reason=None):
        message = ("invalid value {value!r} ({type}) for key {key!r}{reason}"
                   "".format(value=value, type=type(value), key=key,
                             reason=': ' + reason if reason else ''))
        super(InvalidValue, self).__init__(message)


class InvalidKey(IntelMQHarmonizationException):

    def __init__(self, key):
        message = "invalid key %s" % repr(key)
        super(InvalidKey, self).__init__(message)


class KeyExists(IntelMQHarmonizationException):

    def __init__(self, key):
        message = "key %s already exists" % repr(key)
        super(KeyExists, self).__init__(message)


class KeyNotExists(IntelMQHarmonizationException):

    def __init__(self, key):
        message = "key %s not exists" % repr(key)
        super(KeyNotExists, self).__init__(message)
