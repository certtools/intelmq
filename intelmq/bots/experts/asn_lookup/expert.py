# -*- coding: utf-8 -*-
"""
TODO: IPv6
"""
from __future__ import unicode_literals
import sys

import pyasn
import six
from intelmq.lib.bot import Bot


class ASNLookupExpertBot(Bot):

    def init(self):
        try:
            self.database = pyasn.pyasn(self.parameters.database)
        except IOError:
            self.logger.error("pyasn data file does not exist or could not be "
                              "accessed in '%s'" % self.parameters.database)
            self.logger.error("Read 'bots/experts/asn_lookup/README' and "
                              "follow the procedure")
            self.stop()

    def process(self):
        event = self.receive_message()

        if event is None:
            self.acknowledge_message()
            return

        for key in ["source.", "destination."]:

            ip_key = key + "ip"
            asn_key = key + "asn"
            bgp_key = key + "network"

            if not event.contains(ip_key):
                continue

            ip = event.value(ip_key)

            info = self.database.lookup(ip)

            if info:
                if info[0]:
                    event.add(asn_key, six.text_type(info[0]), sanitize=True,
                              force=True)
                if info[1]:
                    event.add(bgp_key, six.text_type(info[1]), sanitize=True,
                              force=True)

        self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = ASNLookupExpertBot(sys.argv[1])
    bot.start()
