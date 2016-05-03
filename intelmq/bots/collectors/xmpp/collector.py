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

import json
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
            self.xmpp = XMPPClientBot(self.parameters.xmpp_user + '@'
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

    def killbot(self):
        self.xmpp.disconnect(wait=True)
        self.logger.info("Disconnected")

    def log_message(self, msg):
        self.logger.debug("XMPP Received Event: %r , from %r", msg['body'],
                          msg['from'])
        self.logger.info("XMPP Event received")

        event = None
        raw_msg = None

        # Try to decode the message as json, it might be an event.
        # if this is not possible treat it as raw.
        # TODO: There might be additional work to decode the message
        # as base64
        try:
            event = json.loads(msg['body'])
        except:
            self.logger.info("XMPP Could not interpret the message as json. "
                             "Treating as Raw")
            self.logger.debug("XMPP I'm not able to tell if it is"
                              "base64 or not!")
            raw_msg = msg['body']

        if event:
            self.send_message(event)
        elif raw_msg:
            report = Report()
            report.add("raw", raw_msg)
            self.send_message(report)


class XMPPClientBot(sleekxmpp.ClientXMPP):
    def __init__(self,
                 jid,
                 password,
                 room,
                 room_nick,
                 room_password,
                 logger):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        self.logger = logger
        self.logger.info("XMPP connected")
        self.xmpp_room = room
        self.xmpp_room_nick = room_nick
        self.xmpp_room_password = room_password

        self.add_event_handler("session_start", self.session_start)

    def session_start(self, event):
        self.send_presence()
        self.logger.debug("XMPP Session started")

        try:
            self.get_roster()
        except sleekxmpp.exception.IqError as err:
            self.logger.error('There was an error getting the roster')
            self.logger.error(err.iq['error']['condition'])
            self.disconnect()
        except sleekxmpp.exceptions.IqTimeout:
            self.logger.error('Server is taking too long to respond')
            self.disconnect()

        if self.xmpp_room:
            self.logger.debug("XMPP Joining room: %s", self.xmpp_room)
            pwd = self.xmpp_room_password if self.xmpp_room_password else ""
            self.plugin['xep_0045'].joinMUC(self.xmpp_room,
                                            self.xmpp_room_nick,
                                            password=pwd,
                                            wait=True)


if __name__ == "__main__":
    bot = XMPPCollectorBot(sys.argv[1])
    bot.start()
