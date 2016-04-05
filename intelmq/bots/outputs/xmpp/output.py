# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys

from sleekxmpp import ClientXMPP

from intelmq.lib.bot import Bot


class XMPP(Bot):

    def init(self):
        self.xmpp = XMPPBot(self.parameters.xmpp_user + '@' + self.parameters.xmpp_server,
                            self.parameters.xmpp_password,
                            self.send_message,
                            self.logger)
        self.xmpp.connect(reattempt=True)
        self.xmpp.process()

    def process(self):
        event = self.receive_message()

        if event is None:
            self.acknowledge_message()

        # TODO: catch appropriate exceptions
        self.xmpp.send_message(mto=self.parameters.xmpp_to_user + '@' + self.parameters.xmpp_to_server,
                               mbody=event.to_json())

        self.acknowledge_message()


class XMPPBot(ClientXMPP):

    def __init__(self, jid, password, send_message, logger):
        ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message_logging)
        self.logger = logger
        self.logger.info("XMPP connected")
        self.send_message = send_message

    def session_start(self, event):
        self.send_presence()

        try:
            self.get_roster()
        except IqError as err:
            self.logger.error('There was an error getting the roster')
            self.logger.error(err.iq['error']['condition'])
            self.disconnect()
        except IqTimeout:
            self.logger.error('Server is taking too long to respond')
            self.disconnect()

    def message_logging(self, msg):

        event = json.loads(msg['body'])
        self.logger.info("Event received from {}".format(msg['from']))
        self.send_message(event)


if __name__ == "__main__":
    bot = XMPP(sys.argv[1])
    bot.start()
