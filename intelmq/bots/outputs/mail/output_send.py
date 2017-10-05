#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
#
# Do not send mails:
# sudo ./output_send.py mail-output-send debug
#
# Do send mails:
# sudo ./output_send.py mail-output-send live
#
# If launched without parameter, it would have never ended (as normal intelmq bot).
#
# ssh -t $USER@proki.csirt.cz 'sudo docker exec -i -t intelmq intelmq.bots.outputs.mail.output_send  mailsend-output-cz dialog'
#
from __future__ import unicode_literals
import csv
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from intelmq.lib.bot import Bot
from intelmq.lib.cache import Cache
from intelmq.lib.message import Event
import json
from base64 import b64decode
import logging
import os
import smtplib
import sys
import time
from collections import namedtuple, OrderedDict
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

Mail = namedtuple('Mail', ["key", "to", "attachment"])

class MailSendOutputBot(Bot):
    def process(self):
        pass

    def set_cache(self):
        self.cache = Cache(
                           self.parameters.redis_cache_host,
                           self.parameters.redis_cache_port,
                           self.parameters.redis_cache_db,
                           self.parameters.redis_cache_ttl
                           )

    def init(self):
        self.set_cache()
        if len(sys.argv) > 2 and sys.argv[2] == "dialog":
            with open(self.parameters.mail_template) as f:
                self.mailContents = f.read()

            print("****** Printing mail queue: ******")
            mails = [m for m in self.prepare_mails()]

            if not len(mails):
                print(" *** No mails in queue ***")
                sys.exit(0);

            while True:
                print("What you would like to do?\n"
                    "* enter for send first mail to tester's address {}.\n"
                    "* 'debug' for sending all the e-mails to tester's address"
                    .format(self.parameters.testing_to))
                if self.parameters.testing_to:
                    print("* 's' for setting other tester's address")
                print("* 'all' for sending all the e-mails\n"
                    "* 'x' to cancel\n"
                    "? ", end="")
                i = input()
                if i == "x":
                    sys.exit(0)
                elif i == "all":
                    for mail in mails:
                        self.send_mail(mail.to, mail.attachment, send=True)
                        self.cache.redis.delete(mail.key)
                    print("{}× mail sent.: {}\n".format(len(mails)))
                    sys.exit(0)
                elif i == "s":
                    print("What e-mail should I use?")
                    self.parameters.testing_to = input()
                elif i in ["","y","debug"]:
                    if not self.parameters.testing_to:
                        print("What e-mail should I use?")
                        self.parameters.testing_to = input()
                    if i in ["","y"]:
                        mail = mails[0]
                        self.send_mail(self.parameters.testing_to, mail.attachment, send=True, intendedto=mail.to)
                        count = 1
                    elif i == "debug":
                        [self.send_mail(self.parameters.testing_to, mail.attachment, send=True, intendedto=mail.to) for mail in mails]
                        count = len(mails)
                    print("{}× mail sent to: {}\n".format(count, self.parameters.testing_to))

        else:
            print("Running forever with no job. Run with 'dialog' parameter.")

    # Sends out all emails
    def prepare_mails(self):
        allowed_fieldnames = ['time.source', 'source.ip', 'classification.taxonomy', 'classification.type',
                              'time.observation', 'source.geolocation.cc', 'source.asn', 'event_description.text',
                              'malware.name', 'feed.name', 'feed.url', 'raw']
        fieldnames_translation = {'time.source': 'time_detected', 'source.ip': 'ip', 'classification.taxonomy': 'class',
                                  'classification.type': 'type', 'time.observation': 'time_delivered',
                                  'source.geolocation.cc': 'country_code', 'source.asn': 'asn',
                                  'event_description.text': 'description', 'malware.name': 'malware',
                                  'feed.name': 'feed_name', 'feed.url': 'feed_url', 'raw': 'raw'}

        for mail_record in self.cache.redis.keys("mail:*"):
            lines = []
            self.logger.debug(mail_record)
            for message in self.cache.redis.lrange(mail_record, 0, -1):
                lines.append(json.loads(str(message,encoding="utf-8")))

            # prepare rows for csv attachment
            fieldnames = set()
            rows_output = []
            for row in lines:
                fieldnames = fieldnames | set(row.keys())
                keys = set(allowed_fieldnames).intersection(row)
                ordered_keys = []
                for field in allowed_fieldnames:
                    if field in keys:
                        ordered_keys.append(field)
                try:
                    row["raw"] = b64decode(row["raw"]).decode("utf-8")
                except: # let the row field as is
                    pass
                rows_output.append(OrderedDict({fieldnames_translation[k]:row[k] for k in ordered_keys}))

            # prepare headers for csv attachment
            ordered_fieldnames = []
            for field in allowed_fieldnames:
                ordered_fieldnames.append(fieldnames_translation[field])

            # write data to csv
            output = StringIO()
            dict_writer = csv.DictWriter(output, fieldnames=ordered_fieldnames)
            dict_writer.writerow(dict(zip(ordered_fieldnames, ordered_fieldnames)))
            dict_writer.writerows(rows_output)

            # send the whole message
            mail = Mail(mail_record, str(mail_record[len("mail:"):], encoding="utf-8"), output.getvalue())
            self.send_mail(mail.to, mail.attachment, send=False)
            yield mail

    #def _hasTestingTo(self):
    #    return hasattr(self.parameters, 'testing_to') and self.parameters.testing_to != ""


    # actual funtion to send email through smtp
    def send_mail(self, emailto, attachmentContents, send=False, intendedto = None):
        emailfrom =  self.parameters.emailFrom
        subject = self.parameters.subject
        server = self.parameters.smtp_server
        text = self.mailContents
        if intendedto:
            subject = subject + " (intended for " + str(intendedto) + ")"
        msg = MIMEMultipart()
        msg["From"] = emailfrom
        msg["Subject"] = subject
        msg["To"] = emailto
        rcpts = [emailto]
        if hasattr(self.parameters, 'bcc') and not intendedto:
            rcpts += self.parameters.bcc # bcc is in fact an independent mail

        if send is True:
            msg.attach(MIMEText(text, "html", "utf-8"))

            maintype, subtype = "text/csv".split("/", 1)
            if maintype == "text":
                attachment = MIMEText(attachmentContents, subtype, "utf-8")
            attachment.add_header("Content-Disposition", "attachment",
                                  filename='proki_{}.csv'.format(time.strftime("%Y%m%d")))
            msg.attach(attachment)

            smtp = smtplib.SMTP(server)
            smtp.sendmail(emailfrom, rcpts, msg.as_string().encode('ascii'))
            smtp.close()
        else:
            print('To: ' + emailto + '; Subject: ' + subject)
            print('Events: ' + str((attachmentContents.count('\n') - 1)))
            print('-------------------------------------------------')

BOT = MailSendOutputBot
