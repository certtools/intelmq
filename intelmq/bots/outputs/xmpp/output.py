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
        def __init__(self,
                     jid,
                     password,
                     room,
                     room_nick,
                     room_password,
                     logger):
            sleekxmpp.ClientXMPP.__init__(self, jid, password)

            self.xmpp_room = room
            self.xmpp_room_nick = room_nick
            self.xmpp_room_password = room_password

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

            self.logger.debug('Room:' + self.xmpp_room)

            if self.xmpp_room: # and self.plugin.get('xep_0045') # this check should also exist!
                self.logger.debug("Joining room: %s." % self.xmpp_room)
                pwd = self.xmpp_room_password if self.xmpp_room_password else ""
                self.plugin['xep_0045'].joinMUC(self.xmpp_room,
                                                self.xmpp_room_nick,
                                                password=pwd,
                                                wait=True)

except ImportError:
    sleekxmpp = None


class XMPPOutputBot(Bot):
    def init(self):
        if sleekxmpp is None:
            self.logger.error('Could not import sleekxmpp. Please install it.')
            self.stop()

        if self.parameters.is_muc:
            self.logger.debug("Trying MUC")
            self.xmpp_room = self.parameters.xmpp_to_user + '@' + self.parameters.xmpp_to_server
            self.xmpp_room_nick = self.parameters.xmpp_user + '@' + self.parameters.xmpp_server
            self.xmpp_room_password = self.parameters.xmpp_room_password
        else:
            self.xmpp_room = None
            self.xmpp_room_nick = None
            self.xmpp_room_password = None

        self.xmpp = XMPPClient(self.parameters.xmpp_user + '@' +
                               self.parameters.xmpp_server,
                               self.parameters.xmpp_password,
                               self.xmpp_room,
                               self.xmpp_room_nick,
                               self.xmpp_room_password,
                               self.logger)
        if self.parameters.ca_certs:
            self.xmpp.ca_certs = self.parameters.ca_certs
        self.xmpp.connect(reattempt=True)
        self.xmpp.process()

        # Add Handlers and register Plugins
        self.xmpp.register_plugin('xep_0030')  # Service Discovery
        self.xmpp.register_plugin('xep_0045')  # Multi-User Chat

    def process(self):
        event = self.receive_message()

        receiver = self.parameters.xmpp_to_user + '@' +\
            self.parameters.xmpp_to_server
        # The Receiver can also be a room.

        jevent = event.to_json(hierarchical=self.parameters.hierarchical_output,
                               with_type=True)

        try:
            # TODO: proper error handling. Right now it cannot be
            # detected if the message was sent successfully.
            if self.parameters.is_muc:
                self.logger.debug("Trying to send to room %s." % self.xmpp_room)
                self.xmpp.send_message(mto=self.xmpp_room, mbody=jevent, mtype='groupchat')
            else:
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
