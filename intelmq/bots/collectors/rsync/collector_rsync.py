# -*- coding: utf-8 -*-
from os import mkdir, path
from subprocess import call

from intelmq import VAR_STATE_PATH
from intelmq.lib.bot import CollectorBot


class RsyncCollectorBot(CollectorBot):
    def init(self):
        self.rsync_data_directory = getattr(self.parameters, 'temp_directory',
                                            path.join(VAR_STATE_PATH, "rsync_collector"))
        try:
            mkdir(self.rsync_data_directory)
        except FileExistsError:
            pass

    def process(self):
        self.logger.info("Updating file {}.".format(self.parameters.file))
        if call(["rsync", path.join(self.parameters.rsync_path, self.parameters.file), self.rsync_data_directory]) != 0:
            raise ValueError("Rsync file {} failed.".format(self.parameters.file))
        report = self.new_report()
        with open(path.join(self.rsync_data_directory, self.parameters.file), "r") as rsync_file:
            report.add("raw", rsync_file.read())
            self.send_message(report)


BOT = RsyncCollectorBot
