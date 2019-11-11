# -*- coding: utf-8 -*-
import csv
import io
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from intelmq.lib.bot import Bot


class SMTPOutputBot(Bot):

    def init(self):
        if getattr(self.parameters, 'ssl', False):
            self.smtp_class = smtplib.SMTP_SSL
        else:
            self.smtp_class = smtplib.SMTP
        self.starttls = getattr(self.parameters, 'starttls', False)
        self.fieldnames = getattr(self.parameters, 'fieldnames')
        if isinstance(self.fieldnames, str):
            self.fieldnames = self.fieldnames.split(',')
        self.username = getattr(self.parameters, 'smtp_username', None)
        self.password = getattr(self.parameters, 'smtp_password', None)
        self.http_verify_cert = getattr(self.parameters, 'http_verify_cert',
                                        True)

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

        with self.smtp_class(self.parameters.smtp_host, self.parameters.smtp_port,
                             **kwargs) as smtp:
            if self.starttls:
                if self.http_verify_cert:
                    smtp.starttls(context=ssl.create_default_context())
                else:
                    smtp.starttls()
            if self.username and self.password:
                smtp.login(user=self.username, password=self.password)
            msg = MIMEMultipart()
            if self.parameters.text:
                msg.attach(MIMEText(self.parameters.text.format(ev=event)))
            msg.attach(MIMEText(attachment, 'csv'))
            msg['Subject'] = self.parameters.subject.format(ev=event)
            msg['From'] = self.parameters.mail_from.format(ev=event)
            msg['To'] = self.parameters.mail_to.format(ev=event)
            recipients = [recipient.format(ev=event)
                          for recipient
                          in self.parameters.mail_to.split(',')]
            smtp.send_message(msg, from_addr=self.parameters.mail_from,
                              to_addrs=recipients)

        self.acknowledge_message()


BOT = SMTPOutputBot
