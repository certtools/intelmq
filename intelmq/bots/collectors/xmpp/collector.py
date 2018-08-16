"""
XMPP Collector Bot
Connects to a XMPP Server and a Room and reads data from the room.
If no room is provided, which is equivalent to an empty string,
it only collects events which were sent to the xmpp user directly.

TLS is used by default.

Tested with Python >= 3.4
Tested with sleekxmpp >= 1.0.0-beta5

Copyright (C) 2016 by Bundesamt für Sicherheit in der Informationstechnik
Software engineering by Intevation GmbH

Parameters:
ca_certs: string to a CA-bundle file or false/empty string for no checks
strip_message: boolean
xmpp_user: string
xmpp_server: string
xmpp_password: boolean
xmpp_room: string
xmpp_room_password: string
xmpp_room_nick: string
pass_full_xml: boolean
strip_message: boolean
xmpp_userlist: array
xmpp_whitelist_mode: boolean
"""


from intelmq.lib.bot import CollectorBot

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

            self.logger = logger
            self.logger.info("Initiated.")
            self.xmpp_room = room
            self.xmpp_room_nick = room_nick
            self.xmpp_room_password = room_password

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

            if self.xmpp_room:  # and self.plugin.get('xep_0045') # this check should also exist!
                self.logger.debug("Joining room: %s.", self.xmpp_room)
                pwd = self.xmpp_room_password if self.xmpp_room_password else ""
                self.plugin['xep_0045'].joinMUC(self.xmpp_room,
                                                self.xmpp_room_nick,
                                                password=pwd,
                                                wait=True)
except ImportError:
    sleekxmpp = None


class XMPPCollectorBot(CollectorBot):

    xmpp = None

    def init(self):
        if sleekxmpp is None:
            raise ValueError('Could not import sleekxmpp. Please install it.')

        # Retrieve Parameters from configuration
        xmpp_user = getattr(self.parameters, "xmpp_user", None)
        xmpp_server = getattr(self.parameters, "xmpp_server", None)
        xmpp_password = getattr(self.parameters, "xmpp_password", None)

        if None in (xmpp_user, xmpp_server, xmpp_password):
            raise ValueError('No User / Password provided.')
        else:
            xmpp_login = xmpp_user + '@' + xmpp_server

        self.userlist = getattr(self.parameters, "xmpp_userlist", [])
        # When configured in manager this is most likely a ,-separated string, we'd like an array
        if type(self.userlist) is str:
            self.userlist = [u.strip() for u in self.userlist.split(",")]
        elif self.userlist is None:  # if value is unset, set to empty list
            self.userlist = []

        self.whitelist_mode = getattr(self.parameters, "xmpp_whitelist_mode", False)

        self.muc = getattr(self.parameters, "use_muc", None)
        xmpp_room = getattr(self.parameters, "xmpp_room", None) if self.muc else None
        xmpp_room_nick = getattr(self.parameters, "xmpp_room_nick", None) if self.muc else None
        xmpp_room_password = getattr(self.parameters, "xmpp_room_password", None) if self.muc else None

        self.pass_full_xml = getattr(self.parameters, "pass_full_xml", None)
        self.strip_message = getattr(self.parameters, "strip_message", None)

        ca_certs = getattr(self.parameters, "ca_certs", None)

        if self.muc and not xmpp_room:
            raise ValueError('No room provided.')

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

            self.xmpp.add_event_handler("message", self.log_message)

        else:
            raise ValueError("Could not connect to XMPP-Server.")

    def process(self):
        # Processing is done by function called from the eventhandler...
        pass

    def shutdown(self):
        if self.xmpp:
            if self.xmpp.disconnect():
                self.logger.info("Disconnected from XMPP Server.")
            else:
                self.logger.error("Could not disconnect from XMPP Server.")
        else:
            self.logger.info("There was no XMPPClient I could stop.")

    def log_message(self, msg):
        # If some exception happens here, the bot would silently fail.
        # We want to know the reason, so we will log the exception manually.
        try:
            # Check if the message was sent by a users that is on
            # the white or blacklist, determine if the message shall
            # be processed.
            if self.muc:
                if msg['mucnick'] not in self.userlist and self.whitelist_mode:
                    # Whitelist-Case
                    return
                elif msg['mucnick'] in self.userlist and not self.whitelist_mode:
                    # Blacklist Case
                    return

            if self.pass_full_xml:
                body = str(msg)
            else:
                if self.strip_message:
                    body = msg['body'].strip()
                else:
                    body = msg['body']

            if len(body) > 400:
                tmp_body = body[:397] + '...'
            else:
                tmp_body = body

            self.logger.debug("Received Stanza: %r from %r.", tmp_body, msg['from'])

            raw_msg = body
            # Read msg-body and add as raw to a new report.
            # now it's up to a parser to do the interpretation of the message.
            if raw_msg:
                report = self.new_report()
                report.add("raw", raw_msg)
                self.send_message(report)
        except Exception:
            self.logger.exception('Error during message handling.')
            raise


BOT = XMPPCollectorBot
