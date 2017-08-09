# -*- coding: utf-8 -*-
"""
SieveExpertBot filters and modifies events based on a specification language similar to mail sieve.

TODO: Document possible necessary configurations.
Parameters:
    file: string
"""
from __future__ import unicode_literals

# imports for additional libraries and intelmq
import os
import intelmq.lib.exceptions as exceptions
from intelmq.lib.bot import Bot
from intelmq.lib.utils import load_configuration
from textx.metamodel import metamodel_from_file
from textx.exceptions import TextXError


class SieveExpertBot(Bot):

    def init(self):
        # read the sieve grammar
        try:
            filename = os.path.join(os.path.dirname(__file__), 'sieve.tx')
            self.metamodel = metamodel_from_file(filename)
        except TextXError as e:
            self.logger.error('Could not process sieve grammar file.')
            self.logger.error(e.message)
            self.stop()

        # validate parameters
        if not os.path.exists(self.parameters.file):
            raise exceptions.InvalidArgument('file', got=self.parameters.file, expected='existing file')

        # parse sieve file
        try:
            self.metamodel.model_from_file(self.parameters.file)
        except TextXError as e:
            self.logger.error('Could not parse sieve file \'%r\'', self.parameters.file)
            self.logger.error(e.message)
            self.stop()


    def process(self):
        event = self.receive_message()

        # implement the logic here

        self.send_message(event)
        self.acknowledge_message()


BOT = SieveExpertBot
