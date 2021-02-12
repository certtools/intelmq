# -*- coding: utf-8 -*-
import csv
import io
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from intelmq.lib.bot import Bot


class SMTPOutputBot(Bot):
    """Send single events as CSV attachment in dynamically formatted e-mails via SMTP"""
    fieldnames: str = "classification.taxonomy,classification.type,classification.identifier,source.ip,source.asn,source.port"
    mail_from: str = "cert@localhost"
    mail_to: str = "{ev[source.abuse_contact]}"
    smtp_host: str = "localhost"
    smtp_password: str = None
    smtp_port: int = None
    smtp_username: str = None
    ssl: bool = False
    starttls: bool = False
    subject: str = "Incident in your AS {ev[source.asn]}"
    text: str = "Dear network owner,\\n\\nWe have been informed that the following device might have security problems.\\n\\nYour localhost CERT"

    username = None
    password = None
    http_verify_cert = True

    def init(self):
        if self.ssl:
            self.smtp_class = smtplib.SMTP_SSL
        else:
            self.smtp_class = smtplib.SMTP
        if isinstance(self.fieldnames, str):
            self.fieldnames = self.fieldnames.split(',')

    def process(self):
        event = self.receive_message()
        event.set_default_value()

        csvfile = io.StringIO()
        writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames,
                                quoting=csv.QUOTE_MINIMAL, delimiter=str(";"),
                                extrasaction='ignore', lineterminator='\n')
        writer.writeheader()
        writer.writerow(event)
        attachment = csvfile.getvalue()

        if self.http_verify_cert and self.smtp_class == smtplib.SMTP_SSL:
            kwargs = {'context': ssl.create_default_context()}
        else:
            kwargs = {}

        with self.smtp_class(self.smtp_host, self.smtp_port, **kwargs) as smtp:
            if self.starttls:
                if self.http_verify_cert:
                    smtp.starttls(context=ssl.create_default_context())
                else:
                    smtp.starttls()
            if self.username and self.password:
                smtp.login(user=self.username, password=self.password)
            msg = MIMEMultipart()
            if self.text is not None:
                msg.attach(MIMEText(self.text.format(ev=event)))
            msg.attach(MIMEText(attachment, 'csv'))
            msg['Subject'] = self.subject.format(ev=event)
            msg['From'] = self.mail_from.format(ev=event)
            msg['To'] = self.mail_to.format(ev=event)
            recipients = [recipient
                          for recipient
                          in self.mail_to.format(ev=event).split(',')]
            smtp.send_message(msg, from_addr=self.mail_from,
                              to_addrs=recipients)

        self.acknowledge_message()


BOT = SMTPOutputBot
