# SPDX-FileCopyrightText: 2018 dargen3
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
import stat
import shlex
from os import mkdir, path, chmod
from subprocess import run, PIPE
from datetime import datetime, timedelta

from intelmq import VAR_STATE_PATH
from intelmq.lib.bot import CollectorBot


class Time(object):
    def __init__(self, delta=None):
        """ Delta is a datetime.timedelta JSON string, ex: '{days=-1}'. """
        self.time = datetime.now()
        if not isinstance(delta, bool):
            self.time += timedelta(**delta)

    def __getitem__(self, timeformat):
        return self.time.strftime(timeformat)


class RsyncCollectorBot(CollectorBot):
    """Collect data with rsync from any resource rsync supports"""
    rsync_path: str = "<path>"
    file: str = "<file>"
    rsync_file_path_formatting: bool = False
    rate_limit: int = 1000
    extra_params: str = None
    private_key: str = None
    private_key_path: str = None
    strict_host_key_checking: bool = False
    temp_directory: str = path.join(VAR_STATE_PATH, "rsync_collector")  # TODO: should be pathlib.Path

    def init(self):
        try:
            mkdir(self.temp_directory)
        except FileExistsError:
            pass

        if self.extra_params:
            self.extra_params = shlex.split(self.extra_params)
        else:
            self.extra_params = []

        if self.private_key and self.private_key_path:
            raise Exception("You must define only one of the variables private_key or private_key_path")

        if self.private_key:
            bot_id = self._Bot__bot_id
            self.privkeydir = path.join(VAR_STATE_PATH, f'privkey_dir_{bot_id}')
            try:
                mkdir(self.privkeydir)
            except FileExistsError:
                pass
            self.private_key_path = path.join(self.privkeydir, 'private.key')

            # privkey format parser, support formats with and without headers, breaklines, etc.
            if '-----' in self.private_key:
                p = self.private_key.split('-----')[2]
            else:
                p = self.private_key
            pb64 = ''.join(p.split())
            fullkey = ['-----BEGIN OPENSSH PRIVATE KEY-----']
            fullkey += [pb64[i:i + 70] for i in range(0, len(pb64), 70)]
            fullkey += ['-----END OPENSSH PRIVATE KEY-----']
            fullkey += ['']
            final_key = '\n'.join(fullkey)

            with open(self.private_key_path, 'w') as f:
                f.write(final_key)
            chmod(self.private_key_path, stat.S_IRUSR | stat.S_IWUSR)

        if self.private_key_path:
            self.strict_host_key_checking_str = 'yes' if self.strict_host_key_checking else 'no'
            self.extra_params += ['-e', f'ssh -i {self.private_key_path} -o StrictHostKeyChecking={self.strict_host_key_checking_str}']

    def process(self):
        formatting = self.rsync_file_path_formatting
        rsync_file = self.file
        rsync_path = self.rsync_path
        if formatting:
            try:
                rsync_file = rsync_file.format(time=Time(formatting))
                rsync_path = rsync_path.format(time=Time(formatting))
            except TypeError:
                self.logger.error(f"Wrongly formatted rsync_file_path_formatting parameter: {formatting}. Should be boolean (False) or a time-delta JSON.")
                raise
            except KeyError:
                self.logger.error(f"Wrongly formatted file '{rsync_file}' or rsync_path '{rsync_path}'. Possible misspell with 'time' on 'formatting' variable.")
                raise
        rsync_full_path = path.join(rsync_path, rsync_file)

        self.logger.info(f"Updating file {rsync_file}.")
        cmd_list = ["rsync"] + self.extra_params + [rsync_full_path, self.temp_directory]
        self.logger.debug(f"Executing command: {cmd_list}.")
        process = run(cmd_list, stderr=PIPE)
        if process.returncode == 0:
            report = self.new_report()
            with open(path.join(self.temp_directory, rsync_file)) as f:
                report.add("raw", f.read())
                self.send_message(report)
        else:
            raise ValueError(f"Rsync on file {rsync_file!r} failed with exitcode \
                                {process.returncode} and stderr {process.stderr!r}.")


BOT = RsyncCollectorBot
