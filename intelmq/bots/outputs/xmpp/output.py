"""
XMPP Output Bot
Connects to a XMPP Server and sends data to a user.

TODO: Introduce Multi User Chat like in XMPP Collector

Requires Python >= 3.4
Requires sleekxmpp >= 1.0.0-beta5

Copyright (C) 2016 by Bundesamt für Sicherheit in der Informationstechnik
Software engineering by Intevation GmbH

Parameters:
xmpp_user: string
xmpp_server: string
xmpp_password: boolean
# TODO xmpp_room: string
# TODO xmpp_room_password: string
# TODO xmpp_room_nick: string
"""
import sys
import json

from intelmq.lib.bot import Bot
from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import XMPPError


class XMPPOutputBot(Bot):

    def init(self):
        self.xmpp = XMPPClientBot(self.parameters.xmpp_user + '@'
                            + self.parameters.xmpp_server,
                            self.parameters.xmpp_password,
                            self.logger)
        self.xmpp.connect(reattempt=True)
        self.xmpp.process()

    def process(self):
        event = self.receive_message()

        receiver = self.parameters.xmpp_to_user + '@' \
                    + self.parameters.xmpp_to_server

        if event is None:
            self.acknowledge_message()
        else:
            jevent = event.to_json()

        try:
            # TODO: proper error handling. Right now it cannot be detected if
            # the message was sent successfully.
            self.logger.debug("XMPP Trying to send Event: %r , to %r",
                            jevent,
                            receiver)
            self.xmpp.send_message(mto=receiver, mbody=jevent)
        except XMPPError as err:
            self.logger.error('There was an error when sending the event')
            self.logger.error(err.iq['error']['condition'])

        self.acknowledge_message()


class XMPPClientBot(ClientXMPP):

    def __init__(self,
                jid,
                password,
                logger):
        ClientXMPP.__init__(self, jid, password)

        self.logger = logger
        self.logger.info("XMPP connected")

        self.add_event_handler("session_start", self.session_start)

    def session_start(self, event):
        self.send_presence()
        self.logger.debug("XMPP Session started")

        try:
            self.get_roster()
        except XMPPError as err:
            self.logger.error('There was an error getting the roster')
            self.logger.error(err.iq['error']['condition'])
            self.disconnect()

if __name__ == "__main__":
    bot = XMPPOutputBot(sys.argv[1])
    bot.start()
