# -*- coding: utf-8 -*-
"""
Using pathlib.Path.touch(path) and os.utime(path) did not work -
the ctime did not change in some cases.
"""
import os
import time

from intelmq.lib.bot import Bot


class TouchOutputBot(Bot):
    file = None

    def process(self):
        self.receive_message()
        ctime = time.time()
        os.utime(self.parameters.path, times=(ctime, ctime))
        self.acknowledge_message()


BOT = TouchOutputBot
