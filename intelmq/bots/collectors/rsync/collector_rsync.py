# -*- coding: utf-8 -*-
from os import mkdir, path
from subprocess import run, PIPE

from intelmq import VAR_STATE_PATH
from intelmq.lib.bot import CollectorBot


class RsyncCollectorBot(CollectorBot):
    "Collect data with rsync from any resource rsync supports"
    file: str = "<file>"
    rate_limit: int = 1000
    rsync_path: str = "<path>"
    temp_directory: str = path.join(VAR_STATE_PATH, "rsync_collector")  # TODO: should be pathlib.Path

    def init(self):
        self.rsync_data_directory = self.temp_directory
        try:
            mkdir(self.rsync_data_directory)
        except FileExistsError:
            pass

    def process(self):
        self.logger.info("Updating file {}.".format(self.file))
        process = run(["rsync", path.join(self.rsync_path, self.file),
                       self.rsync_data_directory],
                      stderr=PIPE)
        if process.returncode != 0:
            raise ValueError("Rsync on file {!r} failed with exitcode {} and stderr {!r}."
                             "".format(self.file,
                                       process.returncode,
                                       process.stderr))
        report = self.new_report()
        with open(path.join(self.rsync_data_directory, self.file), "r") as rsync_file:
            report.add("raw", rsync_file.read())
            self.send_message(report)


BOT = RsyncCollectorBot
