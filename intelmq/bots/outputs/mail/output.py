#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Initiate dialog ex like this:
# ssh -t $USER@proki.csirt.cz 'sudo docker exec -i -t intelmq intelmq.bots.outputs.mail.output_send  mailsend-output-cz cli'
#
from __future__ import unicode_literals

import argparse
import ast
import csv
import datetime
import json
import os
import smtplib
import sys
import time
import zipfile
from base64 import b64decode
from collections import namedtuple, OrderedDict
from email.message import Message
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid

from intelmq.lib.bot import Bot
from intelmq.lib.cache import Cache

from .gpgsafe import GPGSafe

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

Mail = namedtuple('Mail', ["key", "to", "path", "count"])

class MailSendOutputBot(Bot):
    TMP_DIR = "/tmp/intelmq-mails/"

    def process(self):
        message = self.receive_message()
        #mail_rewrite = ast.literal_eval(self.parameters.mail_rewrite)

        self.logger.warning("ZPRAVA..")
        self.logger.debug(message)

        # message.add("source.abuse_contact",u"edvard.rejthar+test_abusemail@nic.cz") # XX nevim, zda nepouzit https://github.com/certtools/intelmq/blob/master/docs/Harmonization-fields.md treba destination.account, nebo source.account
        self.logger.warning("ZPRAVA END..")
        if "source.abuse_contact" in message:
            field = message["source.abuse_contact"]
            self.logger.warning("{}{}".format(self.key, field))
            if field:
                self.logger.warning("edvard field")
                mails = field if type(field) == 'list' else [field]
            for mail in mails:
                self.logger.warning("edvard mails")

                # rewrite destination address
                #if message["source.abuse_contact"] in mail_rewrite:
                #    message.update({"source.abuse_contact": str(mail_rewrite[message["source.abuse_contact"]])})
                #    mail = mail_rewrite[mail]

                self.cache.redis.rpush("{}{}".format(self.key, field), message)
            self.logger.warning("done")

        self.acknowledge_message()

    def set_cache(self):
        self.cache = Cache(
            self.parameters.redis_cache_host,
            self.parameters.redis_cache_port,
            self.parameters.redis_cache_db,
            self.parameters.redis_cache_ttl
        )

    def init(self):
        self.set_cache()
        self.key = "{}:".format(self._Bot__bot_id)
        parser = argparse.ArgumentParser(prog=" ".join(sys.argv[0:1]))
        parser.add_argument('cli', help='initiate cli dialog')
        parser.add_argument('--tester', dest="testing_to", help='tester\'s e-mail')
        parser.add_argument('--ignore-older-than-days', help='1..n skip all events with time.observation older than 1..n day; 0 disabled (allow all)', type=int)
        parser.add_argument("--gpgkey", help="fingerprint of gpg key to be used")
        parser.add_argument("--limit-results", type=int, help="Just send first N mails.")
        parser.parse_args(sys.argv[2:], namespace=self.parameters)

        if self.parameters.cli == "cli":
            self.cli_run()

    def cli_run(self):
        self.parameters.gpg = None
        if self.parameters.gpgkey:
            GPGHOME = "~/.gnupg"
            self.parameters.gpg = GPGSafe(use_agent=False, homedir=GPGHOME)
            if bool(self._sign("test text")):
                print("Successfully loaded GPG key {}".format(self.parameters.gpgkey))
            else:
                print("Error loading GPG key {} from {}".format(self.parameters.gpgkey, os.path.expanduser(GPGHOME)))
                sys.exit(1)

        os.makedirs(self.TMP_DIR, exist_ok=True)
        with open(self.parameters.mail_template) as f:
            self.mail_contents = f.read()
        self.alternative_mail = {}
        if hasattr(self.parameters, "alternative_mails"):
            with open(self.parameters.alternative_mails, "r") as f:
                reader = csv.reader(f, delimiter=",")
                for row in reader:
                    self.alternative_mail[row[0]] = row[1]

        print("Preparing mail queue...")
        mails = [m for m in self.prepare_mails() if m]

        print("")
        if self.parameters.limit_results:
            print("Results limited to {} by flag. ".format(self.parameters.limit_results), end="")

        if not len(mails):
            print(" *** No mails in queue ***")
            sys.exit(0)
        else:
            print("Number of mails in the queue:", len(mails))

        with smtplib.SMTP(self.parameters.smtp_server) as self.smtp:
            while True:
                print("GPG active" if self.parameters.gpgkey else "No GPG")
                print("\nWhat you would like to do?\n"
                      "* enter to send first mail to tester's address {}.\n"
                      "* any mail from above to be delivered to tester's address\n"
                      "* 'debug' to send all the e-mails to tester's address"
                      .format(self.parameters.testing_to))
                if self.parameters.testing_to:
                    print("* 's' for setting other tester's address")
                print("* 'all' for sending all the e-mails\n"
                      "* 'clear' for clearing the queue\n"
                      "* 'x' to cancel\n"
                      "? ", end="")
                i = input()
                if i in ["x", "q"]:
                    sys.exit(0)
                elif i == "all":
                    count = 0
                    for mail in mails:
                        if self.build_mail(mail, send=True):
                            count += 1
                            self.cache.redis.delete(mail.key)
                            if mail.path:
                                os.unlink(mail.path)
                    print("{}× mail sent.\n".format(count))
                    sys.exit(0)
                elif i == "clear":
                    for mail in mails:
                        self.cache.redis.delete(mail.key)
                    print("Queue cleared.")
                    sys.exit(0)
                elif i == "s":
                    self.set_tester()
                elif i in ["", "y"]:
                    self.send_mails_to_tester([mails[0]])
                elif i == "debug":
                    self.send_mails_to_tester(mails)
                else:
                    for mail in mails:
                        if mail.to == i:
                            self.send_mails_to_tester([mail])
                            break
                    else:
                        print("Unknown option.")


    def set_tester(self, force=True):
        if not force and self.parameters.testing_to:
            return
        print("\nWhat e-mail should I use?")
        self.parameters.testing_to = input()

    def send_mails_to_tester(self, mails):
        """
            These mails are going to tester's address. Then prints out their count.
        :param mails: list
        """
        self.set_tester(False)
        count = sum([1 for mail in mails if self.build_mail(mail, send=True, override_to=self.parameters.testing_to)])
        print("{}× mail sent to: {}\n".format(count, self.parameters.testing_to))

    def prepare_mails(self):
        """ Generates Mail objects """
        allowed_fieldnames = ['time.source', 'source.ip', 'classification.taxonomy', 'classification.type',
                              'time.observation', 'source.geolocation.cc', 'source.asn', 'event_description.text',
                              'malware.name', 'feed.name', 'feed.url', 'raw']
        fieldnames_translation = {'time.source': 'time_detected', 'source.ip': 'ip', 'classification.taxonomy': 'class',
                                  'classification.type': 'type', 'time.observation': 'time_delivered',
                                  'source.geolocation.cc': 'country_code', 'source.asn': 'asn',
                                  'event_description.text': 'description', 'malware.name': 'malware',
                                  'feed.name': 'feed_name', 'feed.url': 'feed_url', 'raw': 'raw'}

        for mail_record in self.cache.redis.keys("{}*".format(self.key))[slice(self.parameters.limit_results)]:
            lines = []
            self.logger.debug(mail_record)
            try:
                messages = self.cache.redis.lrange(mail_record, 0, -1)
            except TimeoutError:
                print("!! {} timeouted, too big to read from redis".format(mail_record))
                continue
            for message in messages:
                lines.append(json.loads(str(message, encoding="utf-8")))

            # prepare rows for csv attachment
            threshold = datetime.datetime.now() - datetime.timedelta(
                days=self.parameters.ignore_older_than_days) if getattr(self.parameters, 'ignore_older_than_days',
                                                                        False) else False
            fieldnames = set()
            rows_output = []
            for row in lines:
                # if "feed.name" in row and "NTP-Monitor" in row["feed.name"]: continue
                if threshold and row["time.observation"][:19] < threshold.isoformat()[:19]:
                    # import ipdb; ipdb.set_trace()
                    continue
                fieldnames = fieldnames | set(row.keys())
                keys = set(allowed_fieldnames).intersection(row)
                ordered_keys = []
                for field in allowed_fieldnames:
                    if field in keys:
                        ordered_keys.append(field)
                try:
                    row["raw"] = b64decode(row["raw"]).decode("utf-8").strip().replace("\n", "\\n").replace("\r", "\\r")
                except:  # let the row field as is
                    pass
                rows_output.append(OrderedDict({fieldnames_translation[k]: row[k] for k in ordered_keys}))

            # prepare headers for csv attachment
            ordered_fieldnames = []
            for field in allowed_fieldnames:
                ordered_fieldnames.append(fieldnames_translation[field])

            # write data to csv
            output = StringIO()
            dict_writer = csv.DictWriter(output, fieldnames=ordered_fieldnames)
            dict_writer.writerow(dict(zip(ordered_fieldnames, ordered_fieldnames)))
            dict_writer.writerows(rows_output)

            email_to = str(mail_record[len(self.key):], encoding="utf-8")
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

                if email_to in self.alternative_mail:
                    print("Alternative: instead of {} we use {}".format(email_to, self.alternative_mail[email_to]))
                    email_to = self.alternative_mail[email_to]

            mail = Mail(mail_record, email_to, path, count)
            self.build_mail(mail, send=False)
            if count:
                yield mail

    # def _hasTestingTo(self):
    #    return hasattr(self.parameters, 'testing_to') and self.parameters.testing_to != ""

    def build_mail(self, mail, send=False, override_to=None):
        """ creates a MIME message
        :param mail: Mail object
        :param send: True to send through SMTP, False for just printing the information
        :param override_to: Use this e-mail instead of the one specified in the Mail object
        :return: True if successfully sent.

        """
        if override_to:
            intended_to = mail.to
            email_to = override_to
        else:
            intended_to = None
            email_to = mail.to
        email_from = self.parameters.email_from
        text = self.mail_contents
        try:
            subject = time.strftime(self.parameters.subject)
        except:
            subject = self.parameters.subject
        if intended_to:
            subject += " (intended for {})".format(intended_to)
        else:
            subject += " ({})".format(email_to)
        recipients = [email_to]
        if hasattr(self.parameters, 'bcc') and not intended_to:
            recipients += self.parameters.bcc  # bcc is in fact an independent mail

        if send is True:
            if not mail.count:
                return False

            base_msg = MIMEMultipart()
            base_msg.attach(MIMEText(text, "html", "utf-8"))

            with open(mail.path, "rb") as f:  # plain/text - with open(mail.path,"r") as f: attachment = MIMEText(f.read(), subtype, "utf-8")
                attachment = MIMEApplication(f.read(), "zip")
            attachment.add_header("Content-Disposition", "attachment",
                                  filename='proki_{}.zip'.format(time.strftime("%Y%m%d")))
            base_msg.attach(attachment)
            if self.parameters.gpg:
                msg = MIMEMultipart(_subtype="signed", micalg="pgp-sha1", protocol="application/pgp-signature")
                s = base_msg.as_string().replace('\n', '\r\n')
                signature = self._sign(s)

                if not signature:
                    print("Failed to sign the message for {}".format(email_to))
                    return False
                signature_msg = Message()
                signature_msg['Content-Type'] = 'application/pgp-signature; name="signature.asc"'
                signature_msg['Content-Description'] = 'OpenPGP digital signature'
                signature_msg.set_payload(signature)
                msg.attach(base_msg)
                msg.attach(signature_msg)
            else:
                msg = base_msg

            msg["From"] = email_from
            msg["Subject"] = subject
            msg["To"] = email_to
            msg["Date"] = formatdate(localtime=True)
            msg["Message-ID"] = make_msgid()
            self.smtp.sendmail(email_from, recipients, msg.as_string().encode('ascii'))  # .encode('ascii')
            return True
        else:
            print('To: {}; Subject: {} '.format(email_to, subject), end="")
            if not mail.count:
                print("Won't be send, all events skipped")
            else:
                print('Events: {}, Size: {}'.format(mail.count, os.path.getsize(mail.path)))
            return None

    def _sign(self, s):
        try:
            return str(self.parameters.gpg.sign(s, default_key=self.parameters.gpgkey, detach=True, clearsign=False, passphrase=self.parameters.gpgpass))
        except:
            return ""


BOT = MailSendOutputBot
