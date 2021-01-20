# -*- coding: utf-8 -*-
import csv
import io
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from intelmq.lib.bot import Bot


class SMTPOutputBot(Bot):
    ssl = True
    starttls = False
    fieldnames = None
    username = None
    password = None
    http_verify_cert = True
    smtp_host = None
    smtp_port = None
    text = None
    subject = None
    mail_from = None
    mail_to = None

    def init(self):
        if getattr(self, 'ssl', False):
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
