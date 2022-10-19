# SPDX-FileCopyrightText: 2016 by Bundesamt für Sicherheit in der Informationstechnik
#
# SPDX-License-Identifier: AGPL-3.0-or-later

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
import fcntl

import intelmq.lib.exceptions as exceptions
from intelmq.lib.bot import CollectorBot
from intelmq.lib.splitreports import generate_reports


class FileCollectorBot(CollectorBot):
    """Fetch data from the file system"""
    chunk_replicate_header: bool = True
    chunk_size: int = None
    delete_file: bool = False
    path: str = "/tmp/"  # TODO pathlib.Path
    postfix: str = ".csv"
    rate_limit: int = 300

    def init(self):
        # Test if path is a directory
        if not os.path.isdir(self.path):
            raise exceptions.InvalidArgument('path', got=self.path,
                                             expected="directory")

        if not self.postfix:
            self.logger.warning("No file extension was set. The collector will"
                                " read all files in %s.", self.path)
            if self.delete_file:
                self.logger.error("This configuration would delete all files"
                                  " in %s. I'm stopping now....",
                                  self.path)
                self.stop()

    def process(self):
        self.logger.debug("Started looking for files.")

        if os.path.isdir(self.path):
            path = os.path.abspath(self.path)

            # iterate over all files in dir
            for file in os.listdir(path):
                filename = os.path.join(path, file)
                if os.path.isfile(filename):
                    if fnmatch.fnmatch(file, '*' + self.postfix):
                        self.logger.info("Processing file %r.", filename)

                        template = self.new_report()
                        template.add("feed.url", f"file://localhost{filename}")
                        template.add("extra.file_name", file)

                        try:
                            with open(filename, 'rb') as file_handle:
                                fcntl.flock(file_handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
                                for report in generate_reports(template, file_handle,
                                                               self.chunk_size,
                                                               self.chunk_replicate_header):
                                    self.send_message(report)
                                fcntl.flock(file_handle, fcntl.LOCK_UN)
                        except BlockingIOError:
                            self.logger.info(f"File {filename!r} is locked by another"
                                             " process, skipping.")

                        if self.delete_file:
                            try:
                                os.remove(filename)
                                self.logger.debug("Deleted file: %r.", filename)
                            except PermissionError:
                                self.logger.error("Could not delete file %r.", filename)
                                self.logger.info("Maybe I don't have sufficient rights"
                                                 " on that file?")
                                self.logger.error("Stopping now, to prevent reading this"
                                                  " file again.")
                                self.stop()


BOT = FileCollectorBot
