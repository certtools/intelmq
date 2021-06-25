# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2021 Linköping University <https://liu.se/>
# SPDX-License-Identifier: AGPL-3.0-or-later

import unittest
import json
import base64
from ruamel.yaml import YAML

import intelmq.lib.test as test
from intelmq.bots.outputs.templated_smtp.output import TemplatedSMTPOutputBot


yaml = YAML(typ="safe", pure=True)

SENT_MESSAGE = None
EVENT = {
    "__type": "Event",
    "source.ip": "127.0.0.1",
    "source.url": "http://example.com/",
    "destination.fqdn": "destination.example.com",
    "malware.name": "test-malware",
    "raw": "VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wcyBvdmVyIHRoZSBsYXp5IGRvZy4K"
}
EVENT1 = EVENT.copy()
EVENT1['source.abuse_contact'] = 'one@example.com,two@example.com'


def send_message(*pargs, **kwargs):
    global SENT_MESSAGE
    SENT_MESSAGE = pargs[1], kwargs


@test.skip_exotic()
class TestCustomTemplatedSMTPOutputBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = TemplatedSMTPOutputBot
        attachments = """
- content-type: application/json
  text: |
    {
      "malware": "{{ event['malware.name'] }}",
      {%- set comma = joiner(", ") %}
      {%- for key in event %}
         {%- if key.startswith('source.') %}
      {{ comma() }}"{{ key }}": "{{ event[key] }}"
         {%- endif %}
      {%- endfor %}
    }
  name: report.json
- content-type: text/plain
  text: |
    Malware: {{ event['malware.name'] }}
    System: {{ event['destination.fqdn'] }}
  name: report.txt
- content-type: text/csv
  text: |
    {%- set fields = ["source.ip", "source.port", "source.url"] %}
    {%- set sep = joiner(";") %}
    {%- for field in fields %}{{ sep() }}{{ field }}{%- endfor %}
    {% set sep = joiner(";") %}
    {%- for field in fields %}{{ sep() }}{{ event[field] }}{%- endfor %}
  name: report.csv
"""
        cls.sysconfig = {
            "attachments": yaml.load(attachments),
            "smtp_host": "localhost",
            "body": "URL: {{ event['source.url'] }}",
            "subject": "{{ event['malware.name'] }} on {{ event['destination.fqdn'] }}",
            "mail_from": "myself",
            "mail_to": "you,yourself"
        }

    def test_malformed_attachment_spec(self):
        self.input_message = EVENT
        saved_attachments = self.sysconfig["attachments"]
        self.sysconfig["attachments"] = [
            {
                "content-type": "application/json",
                "name": "report.json"
            }
        ]
        with unittest.mock.patch('smtplib.SMTP.send_message', new=send_message), \
             unittest.mock.patch("smtplib.SMTP.connect", return_value=(220, "Mock server")), \
             unittest.mock.patch('smtplib.SMTP.close'):
            self.run_bot(allowed_error_count=1)
        self.sysconfig["attachments"] = saved_attachments
        self.assertRegexpMatches(self.loglines_buffer,
                                 "ERROR - Attachment does not have a text, ignoring:")

    def test_event(self):
        self.input_message = EVENT
        with unittest.mock.patch('smtplib.SMTP.send_message', new=send_message), \
             unittest.mock.patch("smtplib.SMTP.connect", return_value=(220, "Mock server")), \
             unittest.mock.patch('smtplib.SMTP.close'):
            self.run_bot()

        self.assertEqual(SENT_MESSAGE[0]["Subject"], "test-malware on destination.example.com")
        self.assertEqual(SENT_MESSAGE[0]["From"], "myself")
        self.assertEqual(SENT_MESSAGE[0]["To"], "you, yourself")
        self.assertEqual(SENT_MESSAGE[0].get_payload()[0].get_payload(), "URL: http://example.com/\n")
        self.assertEqual(json.loads(base64.b64decode(SENT_MESSAGE[0].get_payload()[1].get_payload()).decode('utf-8')),
            {
                "malware": "test-malware",
                "source.ip": "127.0.0.1",
                "source.url": "http://example.com/"
            }
        )
        self.assertEqual(base64.b64decode(SENT_MESSAGE[0].get_payload()[2].get_payload()).decode('utf-8'),
"""Malware: test-malware
System: destination.example.com""")
        self.assertEqual(base64.b64decode(SENT_MESSAGE[0].get_payload()[3].get_payload()).decode('utf-8'),
"""source.ip;source.port;source.url
127.0.0.1;;http://example.com/""")
        self.assertEqual({"from_addr": "myself", "to_addrs": ["you", "yourself"]},
                         SENT_MESSAGE[1])

    def test_multiple_recipients_event(self):
        self.input_message = EVENT1

        with unittest.mock.patch("smtplib.SMTP.send_message", new=send_message), \
             unittest.mock.patch("smtplib.SMTP.connect", return_value=(220, "Mock server")), \
             unittest.mock.patch("smtplib.SMTP.close"):
            self.run_bot(parameters={"mail_to": "{{ event['source.abuse_contact'] }}"})

        self.assertEqual(SENT_MESSAGE[0]["Subject"], "test-malware on destination.example.com")
        self.assertEqual(SENT_MESSAGE[0]["From"], "myself")
        self.assertEqual(SENT_MESSAGE[0]["To"], ", ".join(EVENT1["source.abuse_contact"].split(",")))
        self.assertEqual({"from_addr": "myself", "to_addrs": ["one@example.com", "two@example.com"]},
                         SENT_MESSAGE[1])


@test.skip_exotic()
class TestDefaultTemplatedSMTPOutputBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = TemplatedSMTPOutputBot
        cls.sysconfig = {
            "smtp_host": "localhost",
            "mail_from": "myself",
            "mail_to": "you,yourself"
        }

    def test_default_body(self):
        self.input_message = EVENT
        with unittest.mock.patch('smtplib.SMTP.send_message', new=send_message), \
             unittest.mock.patch("smtplib.SMTP.connect", return_value=(220, "Mock server")), \
             unittest.mock.patch('smtplib.SMTP.close'):
            self.run_bot()

        self.assertEqual(SENT_MESSAGE[0]["Subject"], "IntelMQ event")
        self.assertEqual(SENT_MESSAGE[0]["From"], "myself")
        self.assertEqual(SENT_MESSAGE[0]["To"], "you, yourself")
        self.assertEqual(SENT_MESSAGE[0].get_payload()[0].get_payload(), """
source.ip: 127.0.0.1
source.url: http://example.com/
destination.fqdn: destination.example.com
malware.name: test-malware
""")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
