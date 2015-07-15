'''
    IntelMQ Exception Class
'''

class IntelMQException(Exception):

    def __init__(self, message):
        super(IntelMQException, self).__init__(message)


'''
    IntelMQ Exception SubClasses
'''


class InvalidArgument(IntelMQException):

    def __init__(self, argument):
        message = "argument %s is invalid" % repr(argument)
        super(InvalidArgument, self).__init__(message)


class PipelineError(IntelMQException):

    def __init__(self, argument):
        message = "pipeline failed - %s" % repr(argument)
        super(PipelineError, self).__init__(message)


class ConfigurationError(IntelMQException):

    def __init__(self, config, argument):
        message = "%s configuration failed - %s" % (config, repr(argument))
        super(PipelineError, self).__init__(message)
        
class PipelineFactoryError(IntelMQException):
    pass



'''
    IntelMQ Harmonization Exception Class
'''


class IntelMQHarmonizationException(IntelMQException):

    def __init__(self, message):
        super(IntelMQHarmonizationException, self).__init__(message)


'''
    IntelMQ Harmonization Exception SubClasses
'''


class InvalidValue(IntelMQHarmonizationException):

    def __init__(self, key, value):
        message = "invalid value %s (%s) for key %s" % (repr(value), type(value), repr(key))
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
