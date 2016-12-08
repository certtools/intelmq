# -*- coding: utf-8 -*-
import io
import sys
import os

from intelmq.lib.bot import Bot



class FileBot(Bot):

    def init(self):
        self.logger.debug("Opening %s file" % self.parameters.file)
        self.file = io.open(self.parameters.file, mode='at', encoding="utf-8")
        self.logger.info("File %s is open." % self.parameters.file)

    def process(self):
        event = self.receive_message()
        event_data = event.to_json(hierarchical=self.parameters.hierarchical_output)
        self.acknowledge_message()

        try:
            os.stat(self.parameters.file)
        except FileNotFoundError:
            self.init()
        finally:
            self.file.write(event_data)
            self.file.write("\n")
            self.file.flush()


BOT = FileOutputBot
