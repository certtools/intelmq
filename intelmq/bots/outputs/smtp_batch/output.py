# SPDX-FileCopyrightText: 2022 CSIRT.cz <https://csirt.cz>
# SPDX-License-Identifier: AGPL-3.0-or-later
import csv
from dataclasses import dataclass
import datetime
import json
import os
import sys
from tempfile import NamedTemporaryFile
import time
from typing import Any, Optional
import zipfile
from base64 import b64decode
from collections import OrderedDict
from io import StringIO

from redis.exceptions import TimeoutError

from intelmq.lib.bot import Bot
from intelmq.lib.cache import Cache
from intelmq.lib.exceptions import MissingDependencyError

try:
    from envelope import Envelope
except ImportError:
    Envelope = None


@dataclass
class Mail:
    key: str
    to: str
    path: str
    count: int


class SMTPBatchOutputBot(Bot):
    # configurable parameters
    alternative_mails: Optional[str] = None
    bcc: Optional[list] = None
    email_from: str = ""
    gpg_key: Optional[str] = None
    gpg_pass: Optional[str] = None
    mail_template: str = ""
    ignore_older_than_days: Optional[int] = None
    limit_results: Optional[int] = None
    redis_cache_db: int = 15
    redis_cache_host: str = ""
    redis_cache_port: int = 0
    redis_cache_ttl: int = 1728000
    smtp_server: Any = "localhost"
    subject: str = "IntelMQ warning (%Y-%m-%d)"
    attachment_name: str = "intelmq_%Y-%m-%d"
    testing_to: Optional[str] = None
    allowed_fieldnames: list = ['time.source', 'source.ip', 'classification.taxonomy', 'classification.type',
                                'time.observation', 'source.geolocation.cc', 'source.asn', 'event_description.text',
                                'malware.name', 'feed.name', 'feed.url', 'raw']
    fieldnames_translation: dict = {'time.source': 'time_detected', 'source.ip': 'ip', 'classification.taxonomy': 'class',
                                    'classification.type': 'type', 'time.observation': 'time_delivered',
                                    'source.geolocation.cc': 'country_code', 'source.asn': 'asn',
                                    'event_description.text': 'description', 'malware.name': 'malware',
                                    'feed.name': 'feed_name', 'feed.url': 'feed_url', 'raw': 'raw'}

    # private parameters
    mail_contents: str
    alternative_mail: dict = {}
    timeout: list
    cache: Cache
    key: str
    send: bool = False
    cli: bool = False  # whether we are in the CLI mode

    def process(self):
        message = self.receive_message()
        if "source.abuse_contact" in message:
            field = message["source.abuse_contact"]
            for mail in (field if isinstance(field, list) else [field]):
                self.cache.redis.rpush(f"{self.key}{mail}", message.to_json())

        self.acknowledge_message()

    def set_cache(self):
        self.cache = Cache(
            self.redis_cache_host,
            self.redis_cache_port,
            self.redis_cache_db,
            self.redis_cache_ttl
        )

    def init(self):
        if Envelope is None:
            raise MissingDependencyError('envelope', '>=2.0.0')
        self.set_cache()
        self.key = f"{self._Bot__bot_id}:"

    @classmethod
    def run(cls, parsed_args=None):
        if not parsed_args:
            parsed_args = cls._create_argparser().parse_args()

        if parsed_args.cli:
            instance = cls(parsed_args.bot_id)
            [setattr(instance, k, v) for k, v in vars(parsed_args).items()]
            instance.cli_run()
        else:
            super().run(parsed_args=parsed_args)

    @classmethod
    def _create_argparser(cls):
        argparser = super()._create_argparser()
        argparser.add_argument('--cli', help='initiate CLI interface', action="store_true")
        argparser.add_argument('--tester', dest="testing_to", help='tester\'s e-mail')
        argparser.add_argument('--ignore-older-than-days',
                               help='1..n skip all events with time.observation'
                               ' older than 1..n day; 0 disabled (allow all)',
                               type=int)
        argparser.add_argument("--gpg-key", help="fingerprint of gpg key to be used")
        argparser.add_argument("--limit-results", type=int, help="Just send first N mails.")
        argparser.add_argument("--send", help="Sends now, without dialog.", action='store_true')
        return argparser

    def cli_run(self):
        with open(self.mail_template) as f:
            self.mail_contents = f.read()
        if self.alternative_mails:
            with open(self.alternative_mails, "r") as f:
                self.alternative_mail = {row[0]: row[1] for row in csv.reader(f, delimiter=",")}

        print("Preparing mail queue...")
        self.timeout = []
        mails = [m for m in self.prepare_mails() if m]

        print("")
        if self.limit_results:
            print(f"Results limited to {self.limit_results} by flag. ", end="")

        if self.timeout:
            print("Following address has timed out and will not be sent! :(")
            print(self.timeout)

        if not len(mails):
            print(" *** No mails in queue ***")
            sys.exit(0)
        else:
            print("Number of mails in the queue:", len(mails))

        while True:
            print("GPG active" if self.gpg_key else "No GPG")
            print("\nWhat you would like to do?\n"
                  f"* enter to send first mail to tester's address {self.testing_to}.\n"
                  "* any mail from above to be delivered to tester's address\n"
                  "* 'debug' to send all the e-mails to tester's address")
            if self.testing_to:
                print("* 's' for setting other tester's address")
            print("* 'all' for sending all the e-mails\n"
                  "* 'clear' for clearing the queue\n"
                  "* 'x' to cancel\n"
                  "? ", end="")

            if self.send:
                print(" ... Sending now!")
                i = "all"
            else:
                i = input()

            if i in ["x", "q"]:
                sys.exit(0)
            elif i == "all":
                count = 0
                for mail in mails:
                    if self.build_mail(mail, send=True):
                        count += 1
                        print(f"{mail.to} ", end="", flush=True)
                        try:
                            self.cache.redis.delete(mail.key)
                        except TimeoutError:
                            time.sleep(1)
                            try:
                                self.cache.redis.delete(mail.key)
                            except TimeoutError:
                                print(f"\nMail {mail.to} sent but could not be deleted from redis."
                                      f" When launched again, mail will be send again :(.")
                        if mail.path:
                            os.unlink(mail.path)
                print(f"\n{count}× mail sent.\n")
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
        if not force and self.testing_to:
            return
        print("\nWhat e-mail should I use?")
        self.testing_to = input()

    def send_mails_to_tester(self, mails):
        """
            These mails are going to tester's address. Then prints out their count.
        :param mails: list
        """
        self.set_tester(False)
        count = sum([1 for mail in mails if self.build_mail(mail, send=True, override_to=self.testing_to)])
        print(f"{count}× mail sent to: {self.testing_to}\n")

    def prepare_mails(self):
        """ Generates Mail objects """

        for mail_record in self.cache.redis.keys(f"{self.key}*")[slice(self.limit_results)]:
            lines = []
            try:
                messages = self.cache.redis.lrange(mail_record, 0, -1)
            except TimeoutError:
                print(f"Trying again: {mail_record}... ", flush=True)
                for s in range(1, 4):
                    time.sleep(s)
                    try:
                        messages = self.cache.redis.lrange(mail_record, 0, -1)
                        print("... Success!", flush=True)
                        break
                    except TimeoutError:
                        print("... failed ...", flush=True)
                        continue
                else:
                    # visible both warning and print
                    print(f"Warning: {mail_record} timeout, too big to read from redis", flush=True)
                    self.logger.warning(f"Warning: {mail_record} timeout, too big to read from redis")
                    self.timeout.append(mail_record)
                    continue

            lines.extend(json.loads(str(message, encoding="utf-8")) for message in messages)

            # prepare rows for csv attachment
            threshold = datetime.datetime.now() - datetime.timedelta(
                days=self.ignore_older_than_days) if getattr(self, 'ignore_older_than_days',
                                                             False) else False

            # TODO: worthy to generate on the fly https://github.com/certtools/intelmq/pull/2253#discussion_r1172779620
            fieldnames = set()
            rows_output = []
            for row in lines:
                if threshold and row["time.observation"][:19] < threshold.isoformat()[:19]:
                    continue
                fieldnames = fieldnames | set(row.keys())
                keys = set(self.allowed_fieldnames).intersection(row)
                ordered_keys = []
                for field in self.allowed_fieldnames:
                    if field in keys:
                        ordered_keys.append(field)
                try:
                    row["raw"] = b64decode(row["raw"]).decode("utf-8").strip().replace("\n", r"\n").replace("\r", r"\r")
                except (ValueError, KeyError):  # not all events have to contain the "raw" field
                    pass
                rows_output.append(OrderedDict({self.fieldnames_translation[k]: row[k] for k in ordered_keys}))

            # prepare headers for csv attachment
            ordered_fieldnames = []
            for field in self.allowed_fieldnames:
                ordered_fieldnames.append(self.fieldnames_translation[field])

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
                filename = f'{time.strftime("%y%m%d")}_{count}_events'
                path = NamedTemporaryFile().name

                with zipfile.ZipFile(path, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
                    try:
                        zf.writestr(filename + ".csv", output.getvalue())
                    except Exception:
                        self.logger.error(f"Cannot zip mail {mail_record}")
                        continue

                if email_to in self.alternative_mail:
                    print(f"Alternative: instead of {email_to} we use {self.alternative_mail[email_to]}")
                    email_to = self.alternative_mail[email_to]

            mail = Mail(mail_record, email_to, path, count)
            self.build_mail(mail, send=False)
            if count:
                yield mail

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
        email_from = self.email_from
        text = self.mail_contents
        try:
            subject = time.strftime(self.subject)
        except ValueError:
            subject = self.subject
        try:
            attachment_name = time.strftime(self.attachment_name)
        except ValueError:
            attachment_name = self.attachment_name
        if intended_to:
            subject += f" (intended for {intended_to})"
        else:
            subject += f" ({email_to})"

        if send is True:
            if not mail.count:
                return False
            return (Envelope(text)
                    .attach(path=mail.path, name=attachment_name + '.zip')
                    .from_(email_from).to(email_to)
                    .bcc([] if intended_to else getattr(self, 'bcc', []))
                    .subject(subject)
                    .smtp(self.smtp_server)
                    .signature(self.gpg_key, self.gpg_pass)
                    .send())
        else:
            print(f'To: {email_to}; Subject: {subject} ', end="")
            if not mail.count:
                print("Will not be send, all events skipped")
            else:
                print(f'Events: {mail.count}, Size: {os.path.getsize(mail.path)}')
            return None


BOT = SMTPBatchOutputBot
