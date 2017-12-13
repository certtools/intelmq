#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Initiate dialog ex like this:
# ssh -t $USER@proki.csirt.cz 'sudo docker exec -i -t intelmq intelmq.bots.outputs.mail.output_send  mailsend-output-cz dialog'
#
from __future__ import unicode_literals
from base64 import b64decode
import csv
from collections import namedtuple, OrderedDict
import datetime
import json
import argparse
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import logging
import os
import smtplib
import sys
import time
import zipfile
from intelmq.lib.bot import Bot
from intelmq.lib.cache import Cache
from intelmq.lib.message import Event
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

Mail = namedtuple('Mail', ["key", "to", "path", "count"])

class MailSendOutputBot(Bot):
    TMP_DIR = "/tmp/intelmq-mails/"

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
        parser = argparse.ArgumentParser(prog=" ".join(sys.argv[0:1]))
        parser.add_argument('cli', help='initiate cli dialog')
        parser.add_argument('--tester', help='tester\'s e-mail')
        args = parser.parse_args(sys.argv[2:])

        if args.tester:
            self.parameters.testing_to = args.tester

        if args.cli == "cli":
            os.makedirs(self.TMP_DIR, exist_ok=True)
            with open(self.parameters.mail_template) as f:
                self.mailContents = f.read()
            self.alternativeMail = {}
            if self.parameters.alternative_mails:
                with open(self.parameters.alternative_mails,"r") as f:
                    reader = csv.reader(f,delimiter=",")
                    for row in reader:
                        self.alternativeMail[row[0]] = row[1]

            print("Preparing mail queue...")
            mails = [m for m in self.prepare_mails() if m]

            if not len(mails):
                print(" *** No mails in queue ***")
                sys.exit(0);
            
            with smtplib.SMTP(self.parameters.smtp_server) as self.smtp:
                while True:
                    print("What you would like to do?\n"
                        "* enter to send first mail to tester's address {}.\n"
                        "* 'debug' to send all the e-mails to tester's address"
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
                        count = 0
                        for mail in mails:
                            count += 1 if self.send_mail(mail, send=True) else 0
                            self.cache.redis.delete(mail.key)
                            if mail.path:
                                os.unlink(mail.path)
                        print("{}× mail sent.\n".format(count))
                        sys.exit(0)
                    elif i == "s":
                        print("\nWhat e-mail should I use?")
                        self.parameters.testing_to = input()
                    elif i in ["","y","debug"]:
                        if not self.parameters.testing_to:
                            print("\nWhat e-mail should I use?")
                            self.parameters.testing_to = input()
                        if i in ["","y"]:
                            mail = mails[0]
                            self.send_mail(mail, send=True, override_to=self.parameters.testing_to)
                            count = 1
                        elif i == "debug":
                            count = sum([1 for mail in mails if self.send_mail(mail, send=True, override_to=self.parameters.testing_to)])                            
                        print("{}× mail sent to: {}\n".format(count, self.parameters.testing_to))            

        else:
            print("Running forever with no job. Run with 'cli' parameter.")

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
            threshold = datetime.datetime.now()-datetime.timedelta(days=self.parameters.ignore_older_than_days) if getattr(self.parameters, 'ignore_older_than_days', False) else False            
            fieldnames = set()
            rows_output = []                        
            for row in lines:
                #if "feed.name" in row and "NTP-Monitor" in row["feed.name"]: continue                
                if threshold and row["time.observation"][:19] < threshold.isoformat()[:19]:
                        continue
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

            email_to = str(mail_record[len("mail:"):], encoding="utf-8")
            count = len(rows_output)
            if not count:                
                path = None
            else:                
                filename = '{}_{}_events'.format(time.strftime("%y%m%d"), count)
                path = self.TMP_DIR + filename + '_' + email_to + '.zip'

                zf = zipfile.ZipFile(path, mode='w', compression=zipfile.ZIP_DEFLATED)
                try:
                    zf.writestr(filename + ".csv", output.getvalue())
                except:
                    logger.error("Can't zip mail {}".format(mail_record))
                    continue
                finally:
                    zf.close()
                
                if email_to in self.alternativeMail:
                    print("Alternative: instead of {} we use {}".format(email_to, self.alternativeMail[email_to]))
                    email_to = self.alternativeMail[email_to]

            # send the whole message
            mail = Mail(mail_record, email_to, path, count)
            self.send_mail(mail, send=False)
            yield mail

    #def _hasTestingTo(self):
    #    return hasattr(self.parameters, 'testing_to') and self.parameters.testing_to != ""


    # actual funtion to send email through smtp
    def send_mail(self, mail, send=False,  override_to=None):
        if override_to:
            intended_to = mail.to
            email_to = override_to
        else:
            intended_to = None
            email_to = mail.to
        email_from =  self.parameters.emailFrom        
        text = self.mailContents
        try:
            subject = time.strftime(self.parameters.subject)
        except:
            subject = self.parameters.subject
        #if intended_to:
        #    subject += " (intended for {})".format(intended_to)
        #else:
        subject += " ({})".format(email_to)
        msg = MIMEMultipart()
        msg["From"] = email_from
        msg["Subject"] = subject
        msg["To"] = email_to
        rcpts = [email_to]
        if hasattr(self.parameters, 'bcc') and not intended_to:
            rcpts += self.parameters.bcc # bcc is in fact an independent mail

        if send is True:
            if not mail.count:
                return False
            msg.attach(MIMEText(text, "html", "utf-8"))
            with open(mail.path,"rb") as f: # plain/text - with open(mail.path,"r") as f: attachment = MIMEText(f.read(), subtype, "utf-8")
                attachment = MIMEApplication(f.read(), "zip")
            attachment.add_header("Content-Disposition", "attachment",
                                  filename='proki_{}.zip'.format(time.strftime("%Y%m%d")))
            msg.attach(attachment)            
            self.smtp.sendmail(email_from, rcpts, msg.as_string().encode('ascii'))            
            return True
        else:
            print('To: ' + email_to + '; Subject: ' + subject)
            if not mail.count:
                print("Won't be send, all events skipped")
            else:
                print('Events: {}'.format(mail.count))            
            print('-------------------------------------------------')
            return None

BOT = MailSendOutputBot
