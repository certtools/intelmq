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
postfix: string
delete_file: boolean
    default: False
"""

import fnmatch
import os
import sys

import intelmq.lib.exceptions as exceptions
from intelmq.lib.bot import Bot
from intelmq.lib.message import Report
from intelmq.lib.splitreports import generate_reports


class FileCollectorBot(Bot):

    def init(self):
        # Test if path is a directory
        if not os.path.isdir(self.parameters.path):
            raise exceptions.InvalidArgument('path', got=self.parameters.path,
                                             expected="directory")

        if not self.parameters.postfix:
            self.logger.warn("No file extension was set. The collector will"
                             " read all files in %s", self.parameters.path)
            if self.parameters.delete_file:
                self.logger.error("This configuration would delete all files"
                                  " in %s. I'm stopping now....",
                                  self.parameters.path)
                self.stop()

    def process(self):
        self.logger.debug("Started looking for Files")

        if os.path.isdir(self.parameters.path):
            p = os.path.abspath(self.parameters.path)

            # iterate over all files in dir
            for f in os.listdir(p):
                filename = os.path.join(p, f)
                if os.path.isfile(filename):
                    if fnmatch.fnmatch(f, '*' + self.parameters.postfix):
                        self.logger.info("Processing file %r." % filename)

                        template = Report()
                        template.add("feed.name", self.parameters.feed)
                        template.add("feed.url", "file://localhost%s" % filename)
                        template.add("feed.accuracy", self.parameters.accuracy)

                        with open(filename, 'rb') as f:
                            for report in generate_reports(template, f, self.parameters.chunk_size,
                                                           self.parameters.chunk_replicate_header):
                                self.send_message(report)

                        if self.parameters.delete_file:
                            try:
                                os.remove(filename)
                                self.logger.debug("Deleted file: %s" % filename)
                            except PermissionError:
                                self.logger.error("Could not delete file %s" % filename)
                                self.logger.info("Maybe I don't have sufficient rights on that file?")
                                self.logger.error("Stopping now, to prevent reading this file again.")
                                self.stop()

if __name__ == "__main__":
    bot = FileCollectorBot(sys.argv[1])
    bot.start()
