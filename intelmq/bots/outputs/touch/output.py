# SPDX-FileCopyrightText: 2019 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
Using pathlib.Path.touch(path) and os.utime(path) did not work -
the ctime did not change in some cases.
"""
import os
import time

from intelmq.lib.bot import Bot


class TouchOutputBot(Bot):
    """Touch a file for every event received"""
    path = None

    def process(self):
        self.receive_message()
        ctime = time.time()
        os.utime(self.path, times=(ctime, ctime))
        self.acknowledge_message()


BOT = TouchOutputBot
