# SPDX-FileCopyrightText: 2017 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
import csv
import io
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from intelmq.lib.bot import Bot
from typing import Optional


class SMTPOutputBot(Bot):
    """Send single events as CSV attachment in dynamically formatted e-mails via SMTP"""
    fieldnames: str = "classification.taxonomy,classification.type,classification.identifier,source.ip,source.asn,source.port"
    mail_from: str = "cert@localhost"
    mail_to: str = "{ev[source.abuse_contact]}"
    smtp_host: str = "localhost"
    smtp_password: Optional[str] = None
    smtp_port: int = 25
    smtp_username: Optional[str] = None
    ssl: bool = False
    starttls: bool = True
    subject: str = "Incident in your AS {ev[source.asn]}"
    text: str = "Dear network owner,\\n\\nWe have been informed that the following device might have security problems.\\n\\nYour localhost CERT"

    http_verify_cert = True

    def init(self):
        if self.ssl:
            self.smtp_class = smtplib.SMTP_SSL
        else:
            self.smtp_class = smtplib.SMTP
        if self.http_verify_cert and self.smtp_class is smtplib.SMTP_SSL:
            self.kwargs = {'context': ssl.create_default_context()}
        else:
            self.kwargs = {}

        if self.fieldnames and isinstance(self.fieldnames, str):
            self.fieldnames = self.fieldnames.split(',')

    def process(self):
        event = self.receive_message()
        event.set_default_value()

        if self.fieldnames:
            csvfile = io.StringIO()
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames,
                                    quoting=csv.QUOTE_MINIMAL, delimiter=";",
                                    extrasaction='ignore', lineterminator='\n')
            writer.writeheader()
            writer.writerow(event)
            attachment = csvfile.getvalue()

        with self.smtp_class(self.smtp_host, self.smtp_port, **self.kwargs) as smtp:
            if self.starttls:
                self.logger.debug("Issuing STARTTLS with{verify} certificate verification.".format(verify="" if self.http_verify_cert else "out"))
                if self.http_verify_cert:
                    smtp.starttls(context=ssl.create_default_context())
                else:
                    smtp.starttls()
            if self.smtp_username and self.smtp_password:
                self.logger.debug('Authenticating against SMTP server.')
                smtp.login(user=self.smtp_username, password=self.smtp_password)
            msg = MIMEMultipart()
            if self.text is not None:
                msg.attach(MIMEText(self.text.format(ev=event)))
            if self.fieldnames:
                mime_attachment = MIMEText(attachment, 'csv')
                mime_attachment.add_header("Content-Disposition", "attachment", filename="events.csv")
                msg.attach(mime_attachment)
            msg['Subject'] = self.subject.format(ev=event)
            msg['From'] = self.mail_from.format(ev=event)
            msg['To'] = self.mail_to.format(ev=event)
            recipients = [recipient
                          for recipient
                          in self.mail_to.format(ev=event).split(',')]
            self.logger.debug(f'Sending mail to {recipients!r}.')
            smtp.send_message(msg, from_addr=self.mail_from,
                              to_addrs=recipients)

        self.acknowledge_message()


BOT = SMTPOutputBot
