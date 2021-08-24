# -*- coding: utf-8 -*-
"""Templated SMTP output bot

SPDX-FileCopyrightText: 2021 Linköping University <https://liu.se/>
SPDX-License-Identifier: AGPL-3.0-or-later

Sends a MIME Multipart message built from an event and static text
using Jinja2 templates.

Templates are in Jinja2 format with the event provided in the variable
"event". E.g.:

   mail_to: "{{ event['source.abuse_contact'] }}"

See the Jinja2 documentation at https://jinja.palletsprojects.com/ .

Attachments are template strings, especially useful for sending
structured data. E.g. to send a JSON document including "malware.name"
and all other fields starting with "source.":

   attachments:
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

You are responsible for making sure that the text produced by the
template is valid according to the content-type.

SMTP authentication is attempted if both "smtp_username" and
"smtp_password" are provided.

Parameters:

attachments: list of objects with structure:
              - content-type: string, templated, content-type to use.
                text: string, templated, attachment text.
                name: string, templated, filename of attachment.

body: string, optional, default see below, templated, body text.
      The default body template prints every field in the event except
      'raw', in undefined order, one field per line, as "field:
      value".

mail_from: string, templated, sender address.

mail_to: string, templated, recipient addresses, comma-separated.

smtp_host: string, optional, default "localhost", hostname of SMTP
           server.

smtp_password: string, default null, password (if any) for
               authenticated SMTP.

smtp_port: integer, default 25, TCP port to connect to.

smtp_username: string, default null, username (if any) for
               authenticated SMTP.

tls: boolean, default false, whether to use use SMTPS. If true, also
     set smtp_port to the SMTPS port.

starttls: boolean, default true, whether to use opportunistic STARTTLS
          over SMTP.

subject: string, optional, default "IntelMQ event", templated, e-mail
         subject line.

verify_cert: boolean, default true, whether to verify the server
             certificate in STARTTLS or SMTPS.

"""

import io
import smtplib
import ssl
from typing import List, Optional
from email.message import EmailMessage
try:
    from jinja2 import Template
except:
    Template = None

from intelmq.lib.bot import Bot
from intelmq.lib.exceptions import ConfigurationError
from intelmq.lib.exceptions import MissingDependencyError


class TemplatedSMTPOutputBot(Bot):
    smtp_host: str = "localhost"
    smtp_port: int = 25
    ssl: bool = False
    starttls: bool = False
    username: Optional[str] = None
    password: Optional[str] = None
    verify_cert: bool = True
    attachments: List[str] = []
    mail_from: Optional[str] = None
    mail_to: Optional[str] = None
    subject: str = "IntelMQ event"
    body: str = """{%- for field in event %}
    {%- if field != 'raw' %}
{{ field }}: {{ event[field] }}
    {%- endif %}
{%- endfor %}
"""

    def init(self):
        if not Template:
            raise MissingDependencyError("jinja2")

        if self.ssl:
            self.smtp_class = smtplib.SMTP_SSL
        else:
            self.smtp_class = smtplib.SMTP
        if not self.mail_from:
            raise ConfigurationError("Mail", "No sender specified")
        if not self.mail_to:
            raise ConfigurationError("Mail", "No recipient specified")

        if self.username and not self.password:
            raise ConfigurationError("Server", "SMTP username provided, but not password")
        if self.password and not self.username:
            raise ConfigurationError("Server", "SMTP password provided, but not username")

        self.smtp_authentication = self.username and self.password

        self.templates = {
            "subject": Template(self.subject),
            "from": Template(self.mail_from),
            "to": Template(self.mail_to),
            "body": Template(self.body),
            "attachments": []
        }
        for att in self.attachments:
            if "content-type" not in att:
                self.logger.error("Attachment does not have a content-type, ignoring: %s.", att)
                continue
            elif "text" not in att:
                self.logger.error("Attachment does not have a text, ignoring: %s.", att)
                continue
            elif "name" not in att:
                self.logger.error("Attachment does not have a name, ignoring: %s.", att)
                continue
            attachment_template = {
                "content-type": Template(att["content-type"]),
                "text": Template(att["text"]),
                "name": Template(att["name"])
            }
            self.templates["attachments"].append(attachment_template)

    def process(self):
        event = self.receive_message()

        if self.verify_cert and self.smtp_class == smtplib.SMTP_SSL:
            kwargs = {'context': ssl.create_default_context()}
        else:
            kwargs = {}

        with self.smtp_class(self.smtp_host, self.smtp_port,
                             **kwargs) as smtp:
            if self.starttls:
                if self.verify_cert:
                    smtp.starttls(context=ssl.create_default_context())
                else:
                    smtp.starttls()
            if self.smtp_authentication:
                smtp.login(user=self.username, password=self.password)

            msg = EmailMessage()
            msg['Subject'] = self.templates["subject"].render(event=event)
            msg['From'] = self.templates["from"].render(event=event)
            msg['To'] = self.templates["to"].render(event=event)
            msg.add_attachment(self.templates["body"].render(event=event), disposition='inline')

            for att in self.templates["attachments"]:
                msg.add_attachment(att["text"].render(event=event).encode('utf-8'),
                                   maintype=att["content-type"].render(event=event).split('/')[0],
                                   subtype=att["content-type"].render(event=event).split('/')[1],
                                   disposition='attachment',
                                   filename=att["name"].render(event=event))

            recipients = [recipient.strip()
                          for recipient
                          in msg['To'].split(',')]
            self.logger.info("Sending mail to %s.", recipients)
            smtp.send_message(msg, from_addr=msg['From'],
                              to_addrs=recipients)

        self.acknowledge_message()


BOT = TemplatedSMTPOutputBot
