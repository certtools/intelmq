# SPDX-FileCopyrightText: 2022 CSIRT.cz <https://csirt.cz>
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
from pathlib import Path
import time
from types import SimpleNamespace
import unittest

from envelope import Envelope

import intelmq.lib.test as test
from intelmq.bots.outputs.smtp_batch.output import SMTPBatchOutputBot
from intelmq.lib.cache import Cache

SENT_MESSAGES = []  # here we collect e-mail messages there were to be sent
BOT_ID = "test-bot"
IDENTITY1 = 'one@example.com'
KEY1 = f"{BOT_ID}:{IDENTITY1}".encode()
EVENT1 = {'__type': 'Event',
          'source.ip': '127.0.0.1',
          'source.url': 'http://example.com/',
          'source.abuse_contact': IDENTITY1
          }
IDENTITY2 = 'one@example2.com'
KEY2 = f"{BOT_ID}:{IDENTITY2}".encode()
EVENT2 = {'__type': 'Event',
          'source.ip': '127.0.0.2',
          'source.url': 'http://example2.com/',
          'source.abuse_contact': IDENTITY2
          }

REDIS_LOGIN = {"redis_cache_host": "127.0.0.1",
               "redis_cache_port": 6379,
               "redis_cache_db": "14",
               "redis_cache_ttl": ""}
MAIL_TEMPLATE = Path("mail_template.txt")
FROM_IDENTITY = "from-example@example.com"


class TestSMTPBatchOutputBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = SMTPBatchOutputBot
        cls.sysconfig = {"alternative_mails": "",
                         "attachment_name": "events_%Y-%m-%d",
                         "bcc": [],
                         "email_from": FROM_IDENTITY,
                         "gpg_key": "",
                         "gpg_pass": "",
                         "mail_template": str(MAIL_TEMPLATE.resolve()),
                         "ignore_older_than_days": 0,
                         "limit_results": 10,
                         **REDIS_LOGIN,
                         "smtp_server": "localhost",
                         "subject": "Testing subject %Y-%m-%d",
                         "testing_to": ""
                         }

    def compare_envelope(self, envelope: Envelope, subject, message, from_, to):
        self.assertEqual(subject, envelope.subject())
        self.assertEqual(message, envelope.message())
        self.assertEqual(from_, envelope.from_())
        self.assertEqual(to, envelope.to())

    @staticmethod
    def send_message(envelope):
        global SENT_MESSAGES
        SENT_MESSAGES.append(envelope)
        return True  # let's pretend the message sending succeeded

    def test_processing(self):
        redis = Cache(*REDIS_LOGIN.values()).redis
        time_string = time.strftime("%Y-%m-%d")
        message = MAIL_TEMPLATE.read_text()
        self.input_message = (EVENT1, EVENT1, EVENT2, EVENT1)

        # if tests failed before, there might be left records from the last time
        [redis.delete(k) for k in (KEY1, KEY2)]

        # process messages
        self.run_bot(iterations=4)

        # 3 event should be in the DB
        self.assertCountEqual([KEY1, KEY2], redis.keys(f"{self.bot.key}*"))
        self.assertEqual(3, len(redis.lrange(KEY1, 0, -1)))
        self.assertEqual(1, len(redis.lrange(KEY2, 0, -1)))

        # run the CLI interface with the --send parameter, it should send the messages and exit
        with unittest.mock.patch('envelope.Envelope.send', new=self.send_message):
            self.bot.send = True
            self.assertRaises(SystemExit, self.bot.cli_run)

        # compare messages there were to be sent
        self.compare_envelope(
            SENT_MESSAGES[0], f"Testing subject {time_string} ({IDENTITY2})", message, FROM_IDENTITY, [IDENTITY2])
        self.compare_envelope(
            SENT_MESSAGES[1], f"Testing subject {time_string} ({IDENTITY1})", message, FROM_IDENTITY, [IDENTITY1])

        # we expect this ZIP attachment
        self.assertTrue(SENT_MESSAGES[1]
                        .attachments(f"events_{time_string}.zip"))

        # messages should have disappeared from the redis
        self.assertCountEqual([], redis.keys(f"{self.bot.key}*"))        
        

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
