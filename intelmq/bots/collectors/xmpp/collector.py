# -*- coding: utf-8 -*-

import json
import sys

from intelmq.lib.bot import Bot
from intelmq.bots.outputs.xmpp.output import XMPPBot
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
            self.xmpp = sleekxmpp.XMPPBot(self.parameters.xmpp_user + '@' + self.parameters.xmpp_server,
                                self.parameters.xmpp_password,
                                self.send_message,
                                self.logger)
            self.xmpp.connect(reattempt=True)
            self.xmpp.process()

    def killbot(self):
        self.xmpp.disconnect(wait=True)
        self.logger.info("Disconnected")


class XMPPOutputBot(sleekxmpp.ClientXMPP):

    def __init__(self, jid, password, send_message, logger):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message_logging)
        self.logger = logger
        self.logger.info("XMPP connected")
        self.send_message = send_message

    def session_start(self, event):
        self.send_presence()

        try:
            self.get_roster()
        except sleekxmpp.exception.IqError as err:
            self.logger.error('There was an error getting the roster')
            self.logger.error(err.iq['error']['condition'])
            self.disconnect()
        except sleekxmpp.exceptions.IqTimeout:
            self.logger.error('Server is taking too long to respond')
            self.disconnect()

    def message_logging(self, msg):

        event = json.loads(msg['body'])
        self.logger.info("Event received from {}".format(msg['from']))
        self.send_message(event)

if __name__ == "__main__":
    bot = XMPPCollectorBot(sys.argv[1])
    bot.start()
