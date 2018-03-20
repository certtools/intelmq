# -*- coding: utf-8 -*-
"""
Testing HTTP collector
"""

import unittest
import socket
from time import sleep
import threading

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.collectors.tcp.collector import TCPCollectorBot
from intelmq.lib.message import Event

OUTPUT = [{"__type": "Report",
           "feed.name": "Example feed",
           "feed.accuracy": 100.,
           "feed.url": "http://localhost/two_files.tar.gz",
           "raw": utils.base64_encode('bar text\n'),
           },
          {"__type": "Report",
           "feed.name": "Example feed",
           "feed.accuracy": 100.,
           "feed.url": "http://localhost/two_files.tar.gz",
           "raw": utils.base64_encode('foo text\n'),
           },
          ]


# XXX @test.skip_local_web()
class TestTCPCollectorBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for HTTPCollectorBot.
    """

    @classmethod
    def set_bot(cls):
        cls.PORT = 5011
        cls.bot_reference = TCPCollectorBot
        cls.sysconfig = {'http_url': 'http://localhost/two_files.tar.gz',
                         'extract_files': True,
                         'feed': 'Example feed',
                         'ip': "localhost",
                         "port": cls.PORT,
                         "separator": "\n"
                         }

    def test_collecting(self):
        """ Test if correct Events have been produced. """

        def client():
            sleep(1)
            connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connection.connect(("localhost", self.PORT))
            separator = b"\n"
            s = """{"classification.taxonomy": "malicious code","classification.type": "c&c","feed.accuracy": 50.0,"feed.name": "abuse-ch-zeus-tracker-domains","feed.url": "https://zeustracker.abuse.ch/blocklist.php?download=baddomains","malware.name": "zeus","raw": "bHplZGlhbWlrZS50cmFkZQ==","source.fqdn": "lzediamike.trade","time.observation": "2018-03-20T14:05:03+00:00"}"""
            event = Event(Event.unserialize(s))
            data = event.to_json(hierarchical=False)
            l = utils.encode(data) + separator
            connection.sendall(l)
            connection.close()

            #import ipdb; ipdb.set_trace()
            #self.bot.con.close() # XX NEEDED? Will stop without it?
            #self.bot.stop() # XX NEEDED? Will stop without it?

            """
            Chunked test:
            n = 3
            for i in range(2):
                for chunk in [l[i:i + n] for i in range(0, len(l), n)]:
                    print(chunk)
                    self.connection.sendall(chunk)                
            """

        thread = threading.Thread(target=client)
        thread.start()
        self.input_message = None
        self.run_bot()

        # XX asserts...

if __name__ == '__main__':  # pragma: no cover
    unittest.main()


"""
XXXtemporary debug notes: 
m = '{"raw": "YmVzdGRvdmUuaW4udWE=", "feed.url": "https://zeustracker.abuse.ch/blocklist.php?download=baddomains", "classification.type": "c&c", "time.observation": "2018-03-20T14:05:03+00:00", "feed.accuracy": 50.0, "feed.name": "abuse-ch-zeus-tracker-domains", "source.fqdn": "bestdove.in.ua", "malware.name": "zeus", "classification.taxonomy": "malicious code"}'
data = b'{"classification.taxonomy": "malicious code", "time.observation": "2018-03-20T14:05:03+00:00", "feed.name": "abuse-ch-zeus-tracker-domains", "classification.type": "c&c", "feed.accuracy": 50.0, "source.fqdn": "blogerjijer.pw", "malware.name": "zeus", "feed.url": "https://zeustracker.abuse.ch/blocklist.php?download=baddomains", "raw": "YmxvZ2VyamlqZXIucHc="}|'
events = []
for m in data.split(self.separator):
    if m:
        event = Event(Event.unserialize(utils.decode(m)))
        import traceback;
        import ipdb; ipdb.set_trace()
        self.send_message(event)
        super(CollectorBot, self).send_message(event)

debug to send -> use in the tests to send a chunked-messaged
s = "" "{"classification.taxonomy": "malicious code","classification.type": "c&c","feed.accuracy": 50.0,"feed.name": "abuse-ch-zeus-tracker-domains","feed.url": "https://zeustracker.abuse.ch/blocklist.php?download=baddomains","malware.name": "zeus","raw": "bHplZGlhbWlrZS50cmFkZQ==","source.fqdn": "lzediamike.trade","time.observation": "2018-03-20T14:05:03+00:00"}"" "
event = Event(Event.unserialize(s))
data = event.to_json(hierarchical=self.parameters.hierarchical_output)
l = utils.encode(data) + self.separator
n = 3
for chunk in [l[i:i + n] for i in range(0, len(l), n)]:
    print(chunk)
    self.con.sendall(chunk)
"""
