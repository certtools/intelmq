# -*- coding: utf-8 -*-
"""
See README for database download.

TOOD: IPv6
"""
from __future__ import unicode_literals
import sys

from intelmq.lib.bot import Bot


class TorExpertBot(Bot):

    database = list()

    def init(self):
        self.logger.info("Loading TOR exit node IPs.")

        try:
            with open(self.parameters.database) as fp:
                for line in fp:
                    line = line.strip()

                    if len(line) == 0 or line[0] == "#":
                        continue

                    ip_list = line.split("[")[1]
                    ip_list = ip_list.split("]")[0]
                    ip_list = ip_list.split(",")

                    for ip in ip_list:
                        TorExpertBot.database.append(ip.strip())

        except IOError:
            self.logger.critical("TOR rule not defined or failed on open.")
            self.stop()

    def process(self):
        event = self.receive_message()

        if event is None:
            self.acknowledge_message()
            return

        keys = ['source.%s', 'destination.%s']

        for key in keys:
            if event.contains(key % 'ip'):
                if event.value(key % 'ip') in TorExpertBot.database:
                    event.add(key % 'tor_node', u'true')

        self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = TorExpertBot(sys.argv[1])
    bot.start()
