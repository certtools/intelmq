#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
#
# Do not send mails:
# sudo ./output_send.py mail-output-send debug
#
# Do send mails:
# sudo ./output_send.py mail-output-send process
#
# If launched without parameter, it never ends (as normal intelmq bot).
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
import logging
import os
import smtplib
import sys
import time
import collections
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class MailSendOutputBot(Bot):
    def process(self):        
        pass

    debug = False # if True, nothing is sent
    live = False # if True, it exits after mails are sent


    def set_cache(self):
        self.cache = Cache(
                           self.parameters.redis_cache_host,
                           self.parameters.redis_cache_port,
                           self.parameters.redis_cache_db,
                           self.parameters.redis_cache_ttl
                           )

    def init(self):
        self.set_cache()         
        if len(sys.argv) > 2:
            if sys.argv[2] == "debug":
                print("****** Debug session started. ******")
                MailSendOutputBot.debug = True
            elif sys.argv[2] == "live":
                MailSendOutputBot.live = True        
            else:
                return "Unknown state"
            self.send_mails()
            print("MailSendOutputBot done.")
            sys.exit(0)

    # Sends out all emails
    def send_mails(self):        
        self.logger.warning("Going to send mails...")
        allowed_fieldnames = ['time.source', 'source.ip', 'classification.taxonomy', 'classification.type',
                              'time.observation', 'source.geolocation.cc', 'source.asn', 'event_description.text',
                              'malware.name', 'feed.name', 'feed.url', 'raw']
        fieldnames_translation = {'time.source': 'time_detected', 'source.ip': 'ip', 'classification.taxonomy': 'class',
                                  'classification.type': 'type', 'time.observation': 'time_delivered',
                                  'source.geolocation.cc': 'country_code', 'source.asn': 'asn',
                                  'event_description.text': 'description', 'malware.name': 'malware',
                                  'feed.name': 'feed_name', 'feed.url': 'feed_url', 'raw': 'original_base64'}
        with open(self.parameters.mail_template) as f:
            mailContents = f.read()

        for mail_record in self.cache.redis.keys("mail:*"):
            self.logger.warning("Next:")
            self.logger.warning("Mail:" + str(mail_record))
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
                rows_output.append(collections.OrderedDict({fieldnames_translation[k]:row[k] for k in ordered_keys}))

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
            self._send_mail(self.parameters.emailFrom, str(mail_record[len("mail:"):], encoding="utf-8"),
                            'PROKI - upozorneni na nalezene incidenty', mailContents, output.getvalue())
            if not (MailSendOutputBot.debug or hasattr(self.parameters, 'testing_to')):
                self.cache.redis.delete(mail_record)
        self.logger.warning("DONE!")

    # actual funtion to send email through smtp
    def _send_mail(self, emailfrom, emailto, subject, text, fileContents=None):        
        server = self.parameters.smtp_server
        if hasattr(self.parameters, 'testing_to'):
            subject = subject + " (intended for " + str(emailto) + ")"
            emailto = self.parameters.testing_to
        msg = MIMEMultipart()
        msg["From"] = emailfrom
        msg["Subject"] = subject
        msg["To"] = emailto
        #if hasattr(self.parameters, 'bcc') and not hasattr(self.parameters, 'testing_to'):
        #    msg["Bcc"] = self.parameters.bcc
        rcpts = [emailto]
        if hasattr(self.parameters, 'bcc'):
            #msg["Bcc"] = self.parameters.bcc
            rcpts.append(self.parameters.bcc)

        if MailSendOutputBot.live is True:
            msg.attach(MIMEText(text, "plain", "utf-8"))

            maintype, subtype = "text/csv".split("/", 1)
            if maintype == "text":
                attachment = MIMEText(fileContents, _subtype=subtype)
            attachment.add_header("Content-Disposition", "attachment",
                                  filename='proki_{}.csv'.format(time.strftime("%Y%m%d")))
            msg.attach(attachment)
    
            print("NEPOSLU - nefunguje delete!")
            return
            smtp = smtplib.SMTP(server)
            smtp.sendmail(emailfrom, rcpts, msg.as_string().encode('ascii'))
            smtp.close()
        else:
            print('To: ' + emailto + '; Subject: ' + subject)
            print('Events: ' + str((fileContents.count('\n') - 1)))
            print('-------------------------------------------------')


BOT = MailSendOutputBot
