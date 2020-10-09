"""
Testing TCP collector
"""
import socket
import struct
import threading
import unittest
from multiprocessing import Process
from time import sleep

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.collectors.tcp.collector import TCPCollectorBot
from intelmq.bots.outputs.tcp.output import TCPOutputBot
from intelmq.lib.message import Event
from intelmq.lib.message import MessageFactory
from intelmq.lib.utils import base64_decode

PORT = 5011
SEPARATOR = '\n'
INPUT1 = {'classification.taxonomy': 'malicious code',
          'classification.type': 'c2server',
          'feed.name': 'Example feed',
          'feed.accuracy': 100.0,
          'feed.url': 'http://localhost/two_files.tar.gz',
          'raw': utils.base64_encode('bar text\n'),
          'time.observation': '2018-03-20T14:05:03+00:00'}
REPORT1 = {
    'feed.name': 'Example feed',
    'feed.accuracy': 100.0}
# '__type': 'Report'
# 'raw': 'eyJjbGFzc2lmaWNhdGlvbi50YXhvbm9teSI6ICJtYWxpY2lvdXMgY29kZSIsICJjbGFzc2lmaWNhdGlvbi50eXBlIjogImMmYyIsICJmZWVkLm5hbWUiOiAiRXhhbXBsZSBmZWVkIiwgImZlZWQuYWNjdXJhY3kiOiAxMDAuMCwgImZlZWQudXJsIjogImh0dHA6Ly9sb2NhbGhvc3QvdHdvX2ZpbGVzLnRhci5neiIsICJyYXciOiAiWW1GeUlIUmxlSFFLIiwgInRpbWUub2JzZXJ2YXRpb24iOiAiMjAxOC0wMy0yMFQxNDowNTowMyswMDowMCJ9',

INPUT2 = {'feed.name': 'Example feed 2',
          'feed.accuracy': 100.0,
          'feed.url': 'http://localhost/two_files.tar.gz',
          'raw': utils.base64_encode('foo text\n')}
ORIGINAL_DATA = ('some random input{}another line').format(SEPARATOR)

class Client:
    """ You find here an example of a non-intelmq client that might connect to the bot. """

    def _client(self):
        sleep(1)
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect(('localhost', PORT))
        connection.settimeout(1)
        return connection

    def random_client(self):
        connection = self._client()
        d = bytes(ORIGINAL_DATA.split(SEPARATOR)[0], 'UTF-8')
        msg = struct.pack('>I', len(d)) + d
        connection.sendall(msg)
        connection.recv(2)
        d = bytes(ORIGINAL_DATA.split(SEPARATOR)[1], 'UTF-8')
        msg = struct.pack('>I', len(d)) + d
        connection.sendall(msg)
        connection.recv(2)
        connection.close()


class TestTCPOutputBot(test.BotTestCase, unittest.TestCase):
    """ Instance of TCPOutput bot might help to simulate a real world situation with reconnecting etc. """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = TCPOutputBot
        cls.sysconfig = {'hierarchical_output': False,
                         'ip': 'localhost',
                         'port': PORT,
                         'counterpart_is_intelmq': True,
                         }

    def _delayed_start(self):
        sleep(2)
        self.assertEqual = lambda *args, **kwargs: True
        self.run_bot(iterations=len(self.input_message))


class TestTCPCollectorBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for TCPCollectorBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = TCPCollectorBot
        cls.sysconfig = {'http_url': 'http://localhost/two_files.tar.gz', 'extract_files': True,
                         'name': 'Example feed',
                         'ip': 'localhost',
                         'port': PORT
                         }

    def test_random_input(self):
        """ Check how we handle a random input, coming from an unknown source. We should put all the data to report['raw']. """
        thread = threading.Thread(target=Client().random_client)
        thread.start()
        self.run_bot()
        self.assertOutputQueueLen(2)
        generated_report = MessageFactory.unserialize(self.get_output_queue()[1], harmonization=self.harmonization,
                                                      default_type='Event')
        self.assertEqual(base64_decode(generated_report['raw']), ORIGINAL_DATA.split(SEPARATOR)[1])

    def test_intelmq_exchange(self):
        """ Test if correct Events have been produced, sent from a TCP Output of another IntelMQ instance.
        We spawn independent process of the TCPOutput bot that sends a bunch of messages.
        """
        bot = TestTCPOutputBot()
        bot.setUpClass()
        bot.input_message = []
        msg_count = 100
        for i in range(msg_count):
            bot.input_message.append(Event(INPUT1, harmonization=self.harmonization))
        (Process(target=bot._delayed_start)).start()
        self.run_bot()
        self.assertOutputQueueLen(msg_count)

        for i, msg in enumerate(self.get_output_queue()):
            report = MessageFactory.unserialize(msg, harmonization=self.harmonization, default_type='Event')

            output = MessageFactory.unserialize(utils.base64_decode(report["raw"]), harmonization=self.harmonization, default_type='Event')
            self.assertDictEqual(output, INPUT1)

            del report['time.observation']
            del report['raw']
            self.assertDictEqual(report, REPORT1)

    def test_chunked_msg(self):
        """ Test if correct Events have been produced, sent from a TCP Output of another IntelMQ instance,
        when we divide the stream into chunks per n characters and send it 4 times consecutively.
        That way we simulate network throttling. """

        def chunked_process_replacement(self):
            event = self.receive_message()
            data = event.to_json(hierarchical=self.parameters.hierarchical_output)
            d = utils.encode(data)
            msg = struct.pack('>I', len(d)) + d
            chunk_length = 40
            for chunk in [msg[i:i + chunk_length] for i in range(0, len(msg), chunk_length)]:
                self.con.sendall(chunk)
            self.con.recv(2)

        TCPOutputBot._process = TCPOutputBot.process
        TCPOutputBot.process = chunked_process_replacement
        self.test_intelmq_exchange()
        TCPOutputBot.process = TCPOutputBot._process

    def test_multiple_bots(self):
        """ Let's simulate multiple IntelMQ instances are pushing the events at once!
            Every message must be queued.
            Note that if too much clients want connect, connections are refused.
        """
        client_count = 5
        msg_count = 300
        for _ in range(client_count):
            bot = TestTCPOutputBot()
            bot.setUpClass()
            # bot.bot_id = "test-client-{}".format(_)
            bot.input_message = []
            for i in range(msg_count):
                bot.input_message.append(Event(INPUT1, harmonization=self.harmonization))
            Process(target=bot._delayed_start).start()

        thread = threading.Thread(target=Client().random_client)
        thread.start()

        self.run_bot(iterations=client_count + 1)
        self.assertOutputQueueLen(client_count * msg_count + 2)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
