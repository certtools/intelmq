# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys

from intelmq.lib.bot import Bot
import intelmq.lib.utils as utils


class FileBot(Bot):

    def init(self):
        self.logger.debug("Opening %s file" % self.parameters.file)
        self.file = open(self.parameters.file, 'at')
        self.logger.info("File %s is open." % self.parameters.file)

    def process(self):
        event = self.receive_message()

        if event is None:
            self.acknowledge_message()
            return

        if event:
            event_data = event.to_json()
            self.file.write(utils.encode(event_data))
            self.file.write("\n")
            self.file.flush()
        self.acknowledge_message()


if __name__ == "__main__":
    bot = FileBot(sys.argv[1])
    bot.start()
