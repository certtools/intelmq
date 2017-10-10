# -*- coding: utf-8 -*-
import os

from intelmq.lib.bot import Bot

try:
    import pyasn
except ImportError:
    pyasn = None


class ASNLookupExpertBot(Bot):

    def init(self):
        if pyasn is None:
            raise ValueError('Could not import pyasn. Please install it.')

        try:
            self.database = pyasn.pyasn(self.parameters.database)
        except IOError:
            self.logger.error("pyasn data file does not exist or could not be "
                              "accessed in %r.", self.parameters.database)
            self.logger.error("Read 'bots/experts/asn_lookup/README' and "
                              "follow the procedure.")
            self.stop()

    def process(self):
        event = self.receive_message()

        for key in ["source.", "destination."]:

            ip_key = key + "ip"
            asn_key = key + "asn"
            bgp_key = key + "network"

            if ip_key not in event:
                continue

            info = self.database.lookup(event.get(ip_key))

            if info:
                if info[0]:
                    event.add(asn_key, str(info[0]), overwrite=True)
                if info[1]:
                    event.add(bgp_key, str(info[1]), overwrite=True)

        self.send_message(event)
        self.acknowledge_message()

    @staticmethod
    def check(parameters):
        if not os.path.exists(parameters.get('database', '')):
            return [["error", "File given as parameter 'database' does not exist."]]
        try:
            pyasn.pyasn(parameters['database'])
        except Exception as exc:
            return [["error", "Error reading database: %r." % exc]]


BOT = ASNLookupExpertBot
