# -*- coding: utf-8 -*-
"""
See README for database download.
"""

from intelmq.lib.bot import Bot


class TorExpertBot(Bot):

    database = set()

    def init(self):
        self.logger.info("Loading TOR exit node IPs.")

        try:
            with open(self.parameters.database) as fp:
                for line in fp:
                    line = line.strip()

                    if len(line) == 0 or line[0] == "#":
                        continue

                    self.database.add(line)

        except IOError:
            raise ValueError("TOR rule not defined or failed on open.")

        self.overwrite = getattr(self.parameters, 'overwrite', False)

    def process(self):
        event = self.receive_message()

        for key in ["source.", "destination."]:
            if key + 'ip' in event:
                if key + 'tor_node' not in event:
                    if event.get(key + 'ip') in self.database:
                        event.add(key + 'tor_node', True)
                elif key + 'tor_node' in event and self.overwrite:
                    if event.get(key + 'ip') in self.database:
                        event.change(key + 'tor_node', True)

        self.send_message(event)
        self.acknowledge_message()


BOT = TorExpertBot
