"""
XMPP Collector Bot

Requires Python >= 3.4
Connects to a XMPP Server and a Room

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
from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import *


class XMPPCollectorBot(Bot):

    xmpp = None

    def process(self):

        if self.xmpp is None:
            self.xmpp = XMPPBot(self.parameters.xmpp_user + '@' + self.parameters.xmpp_server,
                                self.parameters.xmpp_password,
                                self.parameters.xmpp_room,
                                self.parameters.xmpp_room_nick,
                                self.parameters.xmpp_room_password,
                                self.send_message,
                                self.logger)
            self.xmpp.register_plugin('xep_0030') # Service Discovery
            self.xmpp.register_plugin('xep_0045') # Multi-User Chat
            self.xmpp.connect(reattempt=True)
            self.xmpp.process()

    def killbot(self):
        self.xmpp.disconnect(wait=True)
        self.logger.info("Disconnected")


class XMPPBot(ClientXMPP):

    def __init__(self,jid,password,room,room_nick,room_password,
                send_message,logger):

        ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message_logging)
        self.add_event_handler("groupchat_message", self.message_logging)
        self.logger = logger
        self.logger.info("XMPP connected")
        self.send_message = send_message
        self.xmpp_room = room
        self.xmpp_room_nick = room_nick
        self.xmpp_room_password = room_password

    def session_start(self, event):
        self.send_presence()
        self.logger.debug("XMPP Session started")

        try:
            self.get_roster()
        except IqError as err:
            self.logger.error('There was an error getting the roster')
            self.logger.error(err.iq['error']['condition'])
            self.disconnect()
        except IqTimeout:
            self.logger.error('Server is taking too long to respond')
            self.disconnect()

        if self.xmpp_room:
            self.logger.debug("XMPP Joining room: %s", self.xmpp_room)
            if self.xmpp_room_password:
                self.plugin['xep_0045'].joinMUC(self.xmpp_room,
                                self.xmpp_room_nick,
                                password=self.xmpp_room_password,
                                wait=True)
            else:
                self.plugin['xep_0045'].joinMUC(self.xmpp_room,
                                self.xmpp_room_nick,
                                wait=True)


    def message_logging(self, msg):

        self.logger.debug("XMPP Received Message: %s , from %s", msg['body'],
                        msg['from'])
        self.logger.info("XMPP Event received")
        raw_msg = msg['body']
        report = Report()
        report.add("raw", raw_msg)
        self.send_message(report)

if __name__ == "__main__":
    bot = XMPPCollectorBot(sys.argv[1])
    bot.start()
