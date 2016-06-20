"""
XMPP Collector Bot
Connects to a XMPP Server and a Room and reads data from the room.
If no room is provided, which is equivalent to an empty string,
it only collects events which were sent to the xmpp user directly.

Requires Python >= 3.4
Requires sleekxmpp >= 1.0.0-beta5

Copyright (C) 2016 by Bundesamt für Sicherheit in der Informationstechnik
Software engineering by Intevation GmbH

Parameters:
xmpp_user: string
xmpp_server: string
xmpp_password: boolean
xmpp_room: string
xmpp_room_password: string
xmpp_room_nick: string
"""

import sys

from intelmq.lib.bot import Bot
from intelmq.lib.message import Report

try:
    import sleekxmpp
except ImportError:
    sleekxmpp = None


class XMPPCollectorBot(Bot):
    xmpp = None

    def init(self):
        if sleekxmpp is None:
            self.logger.error('Could not import sleekxmpp. Please install it.')
            self.stop()

    def process(self):
        if self.xmpp is None:
            self.xmpp = XMPPClient(self.parameters.xmpp_user + '@'
                                      + self.parameters.xmpp_server,
                                      self.parameters.xmpp_password,
                                      self.parameters.xmpp_room,
                                      self.parameters.xmpp_room_nick,
                                      self.parameters.xmpp_room_password,
                                      self.logger)
            self.xmpp.connect(reattempt=True)
            self.xmpp.process()

            # Add Handlers and register Plugins
            self.xmpp.register_plugin('xep_0030')  # Service Discovery
            self.xmpp.register_plugin('xep_0045')  # Multi-User Chat
            self.xmpp.add_event_handler("message", self.log_message)
            self.xmpp.add_event_handler("groupchat_message", self.log_message)

    def stop(self):
        if self.xmpp:
            self.xmpp.disconnect()
            self.logger.info("Disconnected from XMPP")

            super(XMPPCollectorBot, self).stop()
        else:
            self.logger.info("There was no XMPPClient I could stop.")

    def log_message(self, msg):
        self.logger.debug("Received Stanza: %r , from %r", msg['body'],
                          msg['from'])
        self.logger.info("Stanza received")

        raw_msg = msg['body']

        # Read msg-body and add as raw to a new report.
        # now it's up to a parser to do the interpretation of the message.
        if raw_msg:
            report = Report()
            report.add("raw", raw_msg)
            self.send_message(report)


class XMPPClient(sleekxmpp.ClientXMPP):
    def __init__(self,
                 jid,
                 password,
                 room,
                 room_nick,
                 room_password,
                 logger):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        self.logger = logger
        self.logger.info("Initiated")
        self.xmpp_room = room
        self.xmpp_room_nick = room_nick
        self.xmpp_room_password = room_password

        self.add_event_handler("session_start", self.session_start)

    def session_start(self, event):
        self.send_presence()
        self.logger.debug("Session started")

        try:
            self.get_roster()
        except sleekxmpp.exceptions.IqError as err:
            self.logger.error('There was an error getting the roster')
            self.logger.error(err.iq['error']['condition'])
            self.disconnect()
        except sleekxmpp.exceptions.IqTimeout:
            self.logger.error('Server is taking too long to respond')
            self.disconnect()

        if self.xmpp_room and self.plugin.get('xep_0045'):
            self.logger.debug("Joining room: %s", self.xmpp_room)
            pwd = self.xmpp_room_password if self.xmpp_room_password else ""
            self.plugin['xep_0045'].joinMUC(self.xmpp_room,
                                            self.xmpp_room_nick,
                                            password=pwd,
                                            wait=True)


if __name__ == "__main__":
    bot = XMPPCollectorBot(sys.argv[1])
    bot.start()
