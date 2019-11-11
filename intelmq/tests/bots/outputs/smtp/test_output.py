# -*- coding: utf-8 -*-
import unittest

import intelmq.lib.test as test
from intelmq.bots.outputs.smtp.output import SMTPOutputBot

SENT_MESSAGE = None
EVENT = {'__type': 'Event',
         'source.ip': '127.0.0.1',
         'source.url': 'http://example.com/'}


def send_message(*pargs, **kwargs):
    global SENT_MESSAGE
    SENT_MESSAGE = pargs[1], kwargs


class TestSMTPOutputBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = SMTPOutputBot
        cls.sysconfig = {"fieldnames": "source.ip,time.source,source.url",
                         "smtp_host": "",
                         "smtp_port": 25,
                         "text": 'foobar',
                         "subject": "type: {ev[classification.type]}",
                         "mail_from": "myself",
                         "mail_to": "you"}

    def test_event(self):
        self.input_message = EVENT
        with unittest.mock.patch('smtplib.SMTP.send_message', new=send_message):
            with unittest.mock.patch('smtplib.SMTP.close'):
                self.run_bot()

        self.assertEqual(SENT_MESSAGE[0]['Subject'], 'type: None')
        self.assertEqual(SENT_MESSAGE[0]['From'], 'myself')
        self.assertEqual(SENT_MESSAGE[0]['To'], 'you')
        self.assertEqual(SENT_MESSAGE[0].get_payload()[0].get_payload(), 'foobar')
        self.assertEqual(SENT_MESSAGE[0].get_payload()[1].get_payload(), '''source.ip;time.source;source.url
127.0.0.1;;http://example.com/
''')
        self.assertEqual({'from_addr': 'myself', 'to_addrs': ['you']},
                         SENT_MESSAGE[1])


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
