# -*- coding: utf-8 -*-
import csv
import io
import smtplib
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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

    def process(self):
        event = self.receive_message()

        csvfile = io.StringIO()
        writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames,
                                quoting=csv.QUOTE_MINIMAL, delimiter=str(";"),
                                extrasaction='ignore', lineterminator='\n')
        writer.writeheader()
        writer.writerow(event)
        attachment = csvfile.getvalue()

        with self.smtp_class(self.parameters.smtp_host, self.parameters.smtp_port) as smtp:
            if self.starttls:
                smtp.starttls()
            if self.username and self.password:
                smtp.auth(smtp.auth_plain, user=self.username, password=self.password)
            msg = MIMEMultipart()
            if self.parameters.text:
                msg.attach(MIMEText(self.parameters.text.format(ev=event)))
            msg.attach(MIMEText(attachment, 'csv'))
            msg['Subject'] = self.parameters.subject.format(ev=event)
            msg['From'] = self.parameters.mail_from.format(ev=event)
            msg['To'] = self.parameters.mail_to.format(ev=event)
            print(msg, file=sys.stderr)
            smtp.send_message(msg, from_addr=self.parameters.mail_from,
                              to_addrs=self.parameters.mail_to.format(ev=event))

        self.acknowledge_message()

BOT = SMTPOutputBot
