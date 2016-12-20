"""
XMPP Output Bot
Connects to a XMPP Server and sends data to a user.

TLS is used by default.

Tested with Python >= 3.4
Tested with sleekxmpp >= 1.0.0-beta5

Copyright (C) 2016 by Bundesamt für Sicherheit in der Informationstechnik
Software engineering by Intevation GmbH

Parameters:
ca_certs: string to a CA-bundle file or false/empty string for no checks
hierarchical_output: boolean (false by default)
xmpp_user: string
xmpp_server: string
xmpp_password: boolean
xmpp_to_user: string
xmpp_to_server: string
"""


from intelmq.lib.bot import Bot

try:
    import sleekxmpp

    class XMPPClient(sleekxmpp.ClientXMPP):
        def __init__(self, jid, password, logger):
            sleekxmpp.ClientXMPP.__init__(self, jid, password)

            self.logger = logger
            self.logger.info("Connected to Server.")

            self.add_event_handler("session_start", self.session_start)

        def session_start(self, event):
            self.send_presence()
            self.logger.debug("Session started.")

            try:
                self.get_roster()
            except sleekxmpp.exceptions.IqError as err:
                self.logger.error('There was an error getting the roster.')
                self.logger.error(err.iq['error']['condition'])
                self.disconnect()
            except sleekxmpp.exceptions.IqTimeout:
                self.logger.error('Server is taking too long to respond.')
                self.disconnect()
except ImportError:
    sleekxmpp = None


class XMPPOutputBot(Bot):
    def init(self):
        if sleekxmpp is None:
            self.logger.error('Could not import sleekxmpp. Please install it.')
            self.stop()

        self.xmpp = XMPPClient(self.parameters.xmpp_user + '@' +
                               self.parameters.xmpp_server,
                               self.parameters.xmpp_password,
                               self.logger)
        if self.parameters.ca_certs:
            self.xmpp.ca_certs = self.parameters.ca_certs
        self.xmpp.connect(reattempt=True)
        self.xmpp.process()

    def process(self):
        event = self.receive_message()

        receiver = self.parameters.xmpp_to_user + '@' +\
            self.parameters.xmpp_to_server

        jevent = event.to_json(hierarchical=self.parameters.hierarchical_output,
                               with_type=True)

        try:
            # TODO: proper error handling. Right now it cannot be
            # detected if the message was sent successfully.
            self.logger.debug("Trying to send Event: %r to %r." % (jevent, receiver))
            self.xmpp.send_message(mto=receiver, mbody=jevent)
        except sleekxmpp.exceptions.XMPPError as err:
            self.logger.error('There was an error when sending the event.')
            self.logger.error(err.iq['error']['condition'])

        self.acknowledge_message()

    def stop(self):
        if self.xmpp:
            self.xmpp.disconnect()
            self.logger.info("Disconnected from XMPP.")

            super(XMPPOutputBot, self).stop()
        else:
            self.logger.info("There was no XMPPClient I could stop.")


BOT = XMPPOutputBot
