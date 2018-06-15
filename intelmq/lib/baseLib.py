# -*- coding: utf-8 -*-

import sys, traceback, os, configparser

from intelmq import (DEFAULT_LOGGING_LEVEL, DEFAULT_LOGGING_PATH,
                     DEFAULTS_CONF_FILE, HARMONIZATION_CONF_FILE,
                     PIPELINE_CONF_FILE, RUNTIME_CONF_FILE, SYSTEM_CONF_FILE)
from intelmq.lib import exceptions, utils

__author__ = 'Jan Göbel <jan-go@gmx.de>'

class baseLib(object):

    def __init__(self, className, logger=None):
        self.__log_buffer = []
        self.parameters = Parameters()
        try:
            version_info = sys.version.splitlines()[0].strip()
            self.__log_buffer.append(('info',
                                  '{} initialized with id and version '
                                  '{} as process {}.'
                                  ''.format(self.__class__.__name__,
                                            version_info, os.getpid())))

            self.__load_defaults_configuration()
            #self.__load_system_configuration() -- deprecated

            if self.parameters.logging_handler == 'syslog':
                syslog = self.parameters.logging_syslog
            else:
                syslog = False

            if logger:
                self.logger = logger
            else:
                self.logger = utils.log(className, syslog=syslog, log_level=self.parameters.logging_level)
                self.logger.debug("Logger initialized.")
        except:
            self.__log_buffer.append(('critical', traceback.format.exec()))
            raise

        self.config = self.__load_library_configuration(className)
        self.logger.info("Finished init of %s!" % (className))

    def __load_library_configuration(self, className):
        """try to load library specific configuration file
        """
        conffile = '/opt/intelmq/etc/%s.conf' % (className)
        if os.path.exists(conffile):
            config = configparser.ConfigParser()
            config.read(conffile)
            self.logger.debug("Configuration successfully parsed (%s)!" % (conffile))
            return config
        self.logger.debug("No configuration file for library %s." % (className))
        return None

    def __load_defaults_configuration(self):
        self.__log_buffer.append(('debug', "Loading defaults configuration."))
        config = utils.load_configuration(DEFAULTS_CONF_FILE)

        setattr(self.parameters, 'testing', False)
        setattr(self.parameters, 'logging_path', DEFAULT_LOGGING_PATH)
        setattr(self.parameters, 'logging_level', DEFAULT_LOGGING_LEVEL)

        for option, value in config.items():
            setattr(self.parameters, option, value)
            self.__log_buffer.append(('debug',
                                      "Defaults configuration: parameter {!r} "
                                      "loaded  with value {!r}.".format(option,
                                                                        value)))

    def __load_system_configuration(self):
        self.__log_buffer.append(('debug', "Loading system configuration."))
        config = utils.load_configuration(SYSTEM_CONF_FILE)

        for option, value in config.items():
            setattr(self.parameters, option, value)
            self.__log_buffer.append(('debug',
                                      "System configuration: parameter {!r} "
                                      "loaded  with value {!r}.".format(option,
                                                                        value)))


    def __load_pipeline_configuration(self):
        self.logger.debug("Loading pipeline configuration.")
        config = utils.load_configuration(PIPELINE_CONF_FILE)

        self.__source_queues = None
        self.__destination_queues = None

        if self.__bot_id in list(config.keys()):

            if 'source-queue' in config[self.__bot_id].keys():
                self.__source_queues = config[self.__bot_id]['source-queue']
                self.logger.debug("Pipeline configuration: parameter "
                                  "'source-queue' loaded with the value {!r}."
                                  "".format(self.__source_queues))

            if 'destination-queues' in config[self.__bot_id].keys():
                self.__destination_queues = config[
                    self.__bot_id]['destination-queues']
                self.logger.debug("Pipeline configuration: parameter"
                                  "'destination-queues' loaded with the value "
                                  "{!r}.".format(", ".join(self.__destination_queues)))

        else:
            self.logger.error("Pipeline configuration: no key "
                              "{!r}.".format(self.__bot_id))
            self.stop()


    def __load_harmonization_configuration(self):
        self.logger.debug("Loading Harmonization configuration.")
        config = utils.load_configuration(HARMONIZATION_CONF_FILE)

        for message_types in config.keys():
            for key in config[message_types].keys():
                for _key in config.keys():
                    if _key.startswith("%s." % key):
                        raise exceptions.ConfigurationError(
                            'harmonization',
                            "Key %s is not valid." % _key)


    def __load_runtime_configuration(self):
        self.logger.debug("Loading runtime configuration.")
        config = utils.load_configuration(RUNTIME_CONF_FILE)

        if self.__bot_id in list(config.keys()):
            for option, value in config[self.__bot_id].items():
                setattr(self.parameters, option, value)
                self.logger.debug("Runtime configuration: parameter {!r} "
                                  "loaded with value {!r}.".format(option, value))


class Parameters(object):
    pass
