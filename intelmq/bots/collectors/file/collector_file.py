# -*- coding: utf-8 -*-
"""
File Collector Bot

Regularly checks a directory and reads files matching an extension from it
It can delete the file if a delete switch was set.
The bot creates on report per file.

Copyright (C) 2016 by Bundesamt für Sicherheit in der Informationstechnik
Software engineering by Intevation GmbH

Parameters:
path: string
extension: string
delete_file: boolean
    default: True
"""

import sys
import os
import fnmatch

from intelmq.lib.bot import Bot
from intelmq.lib.message import Report


class FileCollectorBot(Bot):

    def init(self):
        # Test if path can be accessed
        try:
            if not os.path.isdir(self.parameters.path):
                self.logger.error("The path does not lead to " \
                    "a directory")

        except:
            self.logger.error("The path is not accessible")
            raise exceptions.InvalidArgument('path', got=self.parameters.path)

    def process(self):
        self.logger.debug("Started looking for Files")

        if os.path.isdir(self.parameters.path):
            p = os.path.abspath(self.parameters.path)

            #iterate over all files in dir
            for f in os.listdir(p):
                if fnmatch.fnmatch(f, '*'+self.parameters.extension):
                    filename = p + '/' + f

                    self.logger.debug("Found file to process: %s" %filename)

                    f = open(filename, 'r')

                    report = Report()
                    report.add("raw", f.read())
                    report.add("feed.name", self.parameters.feed)
                    report.add("feed.url", "file:/%s" %filename)
                    report.add("feed.accuracy", self.parameters.accuracy)
                    self.send_message(report)

                    f.close()

                    if self.parameters.delete_file == True:
                        try:
                            os.remove(filename)
                            self.logger.debug("Deleting file: %s" %filename)
                        except:
                            self.logger.error("Could not delete file %s" \
                                %filename)
                            raise

if __name__ == "__main__":
    bot = FileCollectorBot(sys.argv[1])
    bot.start()
