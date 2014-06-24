import sys
import traceback
import xmpp
from lib.bot import *
from lib.utils import *
from lib.event import *
from lib.cache import *

# Required parameters:
# jid
# password
# source_room
# force_tls

class AbuseHelperBot(Bot):

    def handle_message(self, xmpp_connection, message):
        try:
            event = Event.from_unicode(unicode(message.getBody()))
            self.pipeline.send(event)
            print event
        except:
            pass

    def start(self):
        jid = xmpp.JID(self.parameters.jid)
        
        xmpp_connection = xmpp.Client(jid.getDomain(), debug=[])
        connection_result = xmpp_connection.connect()

        if not connection_result:
            # TODO: Log error
            return

        if self.parameters.force_tls == 'true' and connection_result != 'tls':
            # TODO: Log error
            return

        authentication_result = xmpp_connection.auth(jid.getNode(), self.parameters.password)
        if not authentication_result:
            # TODO: Log error
            return

        xmpp_connection.RegisterHandler(name='message', handler=self.handle_message)
        xmpp_connection.sendInitPresence()

        xmpp_connection.send(xmpp.Presence(to='%s@conference.%s/%s' % (self.parameters.source_room, jid.getDomain(), self.bot_id)))

        while True:
            print 'Iteration'
            if not xmpp_connection.isConnected():
                xmpp_connection.reconnectAndReauth()
            else:
                xmpp_connection.Process()

            time.sleep(self.parameters.processing_interval)

if __name__ == "__main__":
    bot = AbuseHelperBot(sys.argv[1])
    bot.start()
