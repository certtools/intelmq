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
xmpp_room: string
xmpp_room_nick: string
xmpp_room_password: string
use_muc: boolean
"""


from intelmq.lib.bot import Bot
from intelmq.lib.exceptions import MissingDependencyError

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
            self.add_event_handler("session_start", self.session_start)

            self.logger.info("Initialized XMPP Client.")

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

            if self.xmpp_room:  # and self.plugin.get('xep_0045') # this check should also exist!
                self.logger.debug("Joining room: %s.", self.xmpp_room)
                pwd = self.xmpp_room_password if self.xmpp_room_password else ""
                self.plugin['xep_0045'].joinMUC(self.xmpp_room,
                                                self.xmpp_room_nick,
                                                password=pwd,
                                                wait=True)

except ImportError:
    sleekxmpp = None


class XMPPOutputBot(Bot):

    xmpp = None

    def init(self):
        self.logger.warning("The output bot 'intelmq.bots.outputs.xmpp.output' "
                            "is deprecated. It will be removed in version 3.0."
                            "Please see https://github.com/certtools/intelmq/blob/"
                            "develop/NEWS.md#xmpp-bots for more details.")
        if sleekxmpp is None:
            raise MissingDependencyError("sleekxmpp")

        # Retrieve Parameters from configuration
        xmpp_user = getattr(self.parameters, "xmpp_user", None)
        xmpp_server = getattr(self.parameters, "xmpp_server", None)
        xmpp_password = getattr(self.parameters, "xmpp_password", None)

        if None in (xmpp_user, xmpp_server, xmpp_password):
            raise ValueError('No User / Password provided.')
        else:
            xmpp_login = xmpp_user + '@' + xmpp_server

        self.muc = getattr(self.parameters, "use_muc", None)
        xmpp_to_user = getattr(self.parameters, "xmpp_to_user", None)
        xmpp_to_server = getattr(self.parameters, "xmpp_to_server", None)
        xmpp_room = getattr(self.parameters, "xmpp_room", None) if self.muc else None
        xmpp_room_nick = getattr(self.parameters, "xmpp_room_nick", None) if self.muc else None
        xmpp_room_password = getattr(self.parameters, "xmpp_room_password", None) if self.muc else None

        ca_certs = getattr(self.parameters, "ca_certs", None)

        # Be sure the receiver was set up
        if not self.muc and None in (xmpp_to_user, xmpp_to_server):
            raise ValueError('No receiver for direct messages provided.')
        else:
            self.xmpp_receiver = xmpp_to_user + '@' +\
                xmpp_to_server

        if self.muc and not xmpp_room:
            raise ValueError('No room provided.')
        else:
            self.xmpp_receiver = xmpp_room

        if self.muc:
            if not xmpp_room_nick:
                # create the room_nick from user and server
                xmpp_room_nick = xmpp_login

        self.xmpp = XMPPClient(xmpp_login, xmpp_password,
                               xmpp_room,
                               xmpp_room_nick,
                               xmpp_room_password,
                               self.logger)

        if ca_certs:
            # Set CA-Certificates
            self.xmpp.ca_certs = ca_certs

        if self.xmpp.connect(reattempt=False):
            self.xmpp.process()
            # Add Handlers and register Plugins
            self.xmpp.register_plugin('xep_0030')  # Service Discovery
            self.xmpp.register_plugin('xep_0045')  # Multi-User Chat
        else:
            raise ValueError("Could not connect to XMPP-Server.")

    def process(self):
        event = self.receive_message()

        jevent = event.to_json(hierarchical=self.parameters.hierarchical_output,
                               with_type=True)

        try:
            # TODO: proper error handling.
            # Right now it cannot be detected if the message was sent successfully.
            if self.muc:
                self.logger.debug("Trying to send to room %s.", self.xmpp_receiver)
                self.xmpp.send_message(mto=self.xmpp_receiver, mbody=jevent, mtype='groupchat')
            else:
                self.logger.debug("Trying to send to %s.", self.xmpp_receiver)
                self.xmpp.send_message(mto=self.xmpp_receiver, mbody=jevent)
        except sleekxmpp.exceptions.XMPPError as err:
            self.logger.error('There was an error when sending the event.')
            self.logger.error(err.iq['error']['condition'])

        self.acknowledge_message()

    def shutdown(self):
        if self.xmpp:
            if self.xmpp.disconnect():
                self.logger.info("Disconnected from XMPP Server.")
            else:
                self.logger.error("Could not disconnect from XMPP Server.")
        else:
            self.logger.info("There was no XMPPClient I could stop.")


BOT = XMPPOutputBot
