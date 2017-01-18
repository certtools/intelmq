# -*- coding: utf-8 -*-
import socket

from intelmq.lib.bot import Bot


class GethostbynameExpertBot(Bot):

    def process(self):
        event = self.receive_message()

        for key in ["source.", "destination."]:
            key_fqdn = key + "fqdn"
            key_ip = key + "ip"
            if key_fqdn not in event:
                continue
            if key_ip in event:
                continue
            ip = socket.gethostbyname(event.get(key_fqdn))
            event.add(key_ip, ip, raise_failure=False)

        self.send_message(event)
        self.acknowledge_message()


BOT = GethostbynameExpertBot
