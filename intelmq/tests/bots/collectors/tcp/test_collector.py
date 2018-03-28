# -*- coding: utf-8 -*-
"""
Testing HTTP collector
"""

import socket
import threading
import unittest
from time import sleep

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.collectors.tcp.collector import TCPCollectorBot
from intelmq.lib.message import Event
from intelmq.lib.message import MessageFactory
from intelmq.lib.utils import base64_decode

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

USECASE1 = {"classification.taxonomy": "malicious code", "classification.type": "c&c", "feed.accuracy": 50.0,
            "feed.name": "abuse-ch-zeus-tracker-domains",
            "feed.url": "https://zeustracker.abuse.ch/blocklist.php?download=baddomains",
            "malware.name": "zeus", "raw": "bHplZGlhbWlrZS50cmFkZQ==", "source.fqdn": "lzediamike.trade",
            "time.observation": "2018-03-20T14:05:03+00:00"}

INPUT1 = {"classification.taxonomy": "malicious code",
          "classification.type": "c&c",
          "feed.name": "Example feed",
          "feed.accuracy": 100.,
          "feed.url": "http://localhost/two_files.tar.gz",
          "raw": utils.base64_encode('bar text\n'),
          "time.observation": "2018-03-20T14:05:03+00:00"
          }
REPORT1 = {
    'raw': 'eyJjbGFzc2lmaWNhdGlvbi50YXhvbm9teSI6ICJtYWxpY2lvdXMgY29kZSIsICJjbGFzc2lmaWNhdGlvbi50eXBlIjogImMmYyIsICJmZWVkLm5hbWUiOiAiRXhhbXBsZSBmZWVkIiwgImZlZWQuYWNjdXJhY3kiOiAxMDAuMCwgImZlZWQudXJsIjogImh0dHA6Ly9sb2NhbGhvc3QvdHdvX2ZpbGVzLnRhci5neiIsICJyYXciOiAiWW1GeUlIUmxlSFFLIiwgInRpbWUub2JzZXJ2YXRpb24iOiAiMjAxOC0wMy0yMFQxNDowNTowMyswMDowMCJ9',
    'feed.name': 'Example feed', 'feed.accuracy': 100.0}

INPUT2 = {
    "feed.name": "Example feed",
    "feed.accuracy": 100.,
    "feed.url": "http://localhost/two_files.tar.gz",
    "raw": utils.base64_encode('foo text\n'),
}


@test.skip_local_web()
class TestIntelMQCollectorBot(test.BotTestCase, unittest.TestCase):
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
        cls.separator = b"\n"

    def _client(self):
        sleep(1)
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect(("localhost", self.PORT))
        return connection

    def _test_collecting_single_message(self):
        """ Test if correct Events have been produced. """

        def client():
            data = Event(INPUT1).to_json(hierarchical=False)
            text = utils.encode(data) + self.separator

            connection = self._client()
            connection.sendall(text)
            connection.close()

        thread = threading.Thread(target=client)
        thread.start()
        self.input_message = None
        self.run_bot()

        self.assertOutputQueueLen(1)
        line = self.get_output_queue()[0]
        generated_report = MessageFactory.unserialize(line, harmonization=self.harmonization, default_type='Event')
        original_message = MessageFactory.unserialize(base64_decode(generated_report["raw"]), harmonization=self.harmonization,
                                               default_type='Event')
        self.assertDictEqual(original_message, INPUT1)
        del generated_report["time.observation"]
        self.assertDictEqual(generated_report, REPORT1)

    def _test_collecting_chunked_messages(self):
        """ Divide a message into chunks per n characters and send it 4 times consecutively. """

        def client():
            connection = self._client()
            data = Event(INPUT2).to_json(hierarchical=False)
            stream = utils.encode(data) + self.separator

            n = 3
            for i in range(4):
                for chunk in [stream[i:i + n] for i in range(0, len(stream), n)]:
                    connection.sendall(chunk)
            connection.close()

        thread = threading.Thread(target=client)
        thread.start()
        self.input_message = None
        self.run_bot()

        self.assertOutputQueueLen(4)
        line = self.get_output_queue()[2]
        generated_report = MessageFactory.unserialize(line, harmonization=self.harmonization, default_type='Event')
        original_message = MessageFactory.unserialize(base64_decode(generated_report["raw"]), harmonization=self.harmonization,
                                               default_type='Event')
        self.assertDictEqual(original_message, INPUT2)

    def test_invalid_input(self):
        """ Check how we handle an invalid input. """

        def client():
            connection = self._client()
            data = Event(INPUT2).to_json(hierarchical=False)
            stream = b"some invalid input" + self.separator
            connection.sendall(stream)
            connection.close()

        thread = threading.Thread(target=client)
        thread.start()
        self.input_message = None
        self.run_bot()

        import ipdb; ipdb.set_trace()

        self.assertOutputQueueLen(4)
        line = self.get_output_queue()[2]
        generated_report = MessageFactory.unserialize(line, harmonization=self.harmonization, default_type='Event')
        original_message = MessageFactory.unserialize(base64_decode(generated_report["raw"]), harmonization=self.harmonization,
                                               default_type='Event')
        self.assertDictEqual(original_message, INPUT2)


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
