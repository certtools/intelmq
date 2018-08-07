# -*- coding: utf-8 -*-
import os
from intelmq.lib.bot import CollectorBot

class RsyncCollectorBot(CollectorBot):
    def process(self):
        self.logger.info("Updating file {}.".format(self.parameters.file))
        os.system("rsync {}/{} {}".format(self.parameters.rsync_path, self.parameters.file, os.path.dirname(__file__)))
        report = self.new_report()
        with open("{}/{}".format("/".join(os.path.abspath(__file__).split("/")[:-1]), self.parameters.file), "r") as rsync_file:
            report.add("raw", rsync_file.read())
            self.send_message(report)

BOT = RsyncCollectorBot


