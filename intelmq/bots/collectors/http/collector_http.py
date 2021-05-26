# SPDX-FileCopyrightText: 2015 National CyberSecurity Center
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
HTTP collector bot

Parameters:
http_url: string
http_header: dictionary
    default: {}
http_verify_cert: boolean
    default: True
extract_files: value used to extract files from downloaded compressed file
    default: None
    all: True; some: string with file names separated by ,
http_url_formatting: bool|json to turn on time formatting (and to specify delta to current time)
http_username, http_password: string
http_proxy, https_proxy: string
http_timeout_sec: tuple of two floats or float
http_timeout_max_tries: an integer depicting how often a connection attempt is retried
verify_pgp_signatures: whether to download and check file signatures
    default: False
signature_url: string
signature_url_formatting: the same as http_url_formatting
gpg_keyring: none (defaults to user's GPG keyring) or string (path to keyring file)
"""
from datetime import datetime, timedelta

from intelmq.lib.bot import CollectorBot
from intelmq.lib.mixins import HttpMixin
from intelmq.lib.utils import unzip
from intelmq.lib.exceptions import MissingDependencyError

try:
    import gnupg
    import tempfile
except ImportError:
    gnupg = None


class Time(object):
    def __init__(self, delta=None):
        """ Delta is a datetime.timedelta JSON string, ex: '{"days"=-1}'. """
        self.time = datetime.now()
        if not isinstance(delta, bool):
            self.time += timedelta(**delta)

    def __getitem__(self, timeformat):
        return self.time.strftime(timeformat)


class HTTPCollectorBot(CollectorBot, HttpMixin):
    """Fetch reports from an URL"""
    extract_files: bool = False
    gpg_keyring: str = None  # TODO: pathlib.Path
    http_password: str = None
    http_url: str = "<insert url of feed>"
    http_url_formatting: bool = False
    http_username: str = None
    rate_limit: int = 3600
    signature_url: str = None
    signature_url_formatting: bool = False
    ssl_client_certificate: str = None  # TODO: pathlib.Path
    verify_pgp_signatures: bool = False

    def init(self):
        self.use_gpg = self.verify_pgp_signatures
        if self.use_gpg and gnupg is None:
            raise MissingDependencyError("gnupg")
        else:
            self.logger.info('PGP signature verification is active.')

    def process(self):
        formatting = self.http_url_formatting
        if formatting:
            http_url = self.format_url(self.http_url, formatting)
        else:
            http_url = self.http_url

        self.logger.info("Downloading report from %r.", http_url)

        resp = self.http_get(http_url)

        if resp.status_code // 100 != 2:
            self.logger.debug('Request headers: %r.', resp.request.headers)
            self.logger.debug('Request body: %r.', resp.request.body)
            self.logger.debug('Response headers: %r.', resp.headers)
            self.logger.debug('Response body: %r.', resp.text)
            raise ValueError('HTTP response status code was %i.' % resp.status_code)

        self.logger.info("Report downloaded.")

        # PGP verification
        if self.use_gpg:
            result = self.verify_signature(data=resp.content)

            if not result:
                # Errors have been logged by the verify_signature function.
                return

            if not result.valid:
                self.logger.error("Signature for key {0.key_id} is not valid: {0.status}. Report rejected.".format(result))
                return

            if result.trust_level < 1:
                self.logger.debug("Trust level not defined for key {}.".format(result.key_id))
            elif result.trust_level < 3:
                self.logger.debug("Low trust level for key {0.key_id}: {0.trust_level}.".format(result))

            self.logger.info("PGP signature checked with key {0.key_id}: {0.status}.".format(result))

        # process reports
        raw_reports = []
        if not self.extract_files:
            try:
                raw_reports = tuple(unzip(resp.content, True, try_gzip=False,
                                          try_tar=False, logger=self.logger,
                                          return_names=True))
            except ValueError:
                raw_reports.append((None, resp.text))
            else:
                self.logger.info('Extracting files: '
                                 "'%s'.", "', '".join([file_name
                                                       for file_name, _
                                                       in raw_reports]))
        else:
            raw_reports = unzip(resp.content, self.extract_files,
                                return_names=True, logger=self.logger)

        for file_name, raw_report in raw_reports:
            report = self.new_report()
            report.add("raw", raw_report)
            report.add("feed.url", http_url)
            if file_name:
                report.add("extra.file_name", file_name)
            self.send_message(report)

    def format_url(self, url: str, formatting) -> str:
        try:
            return self.http_url.format(time=Time(formatting))
        except TypeError:
            self.logger.error(
                "Wrong formatting parameter: %s. Should be boolean or a time-delta JSON.",
                formatting
            )
            raise
        except KeyError:
            self.logger.error(
                "Wrongly formatted url parameter: %s. Possible misspell with 'time' variable.",
                self.http_url
            )
            raise

    def verify_signature(self, data: bytes):
        """
        Download signature file and verify the report data.
        """
        # get PGP parameters
        formatting = self.signature_url_formatting
        if formatting:
            http_url = self.format_url(self.signature_url, formatting)
        else:
            http_url = self.signature_url

        # download signature file
        self.logger.info("Downloading PGP signature from {}.".format(http_url))

        resp = self.http_get(http_url)
        if resp.status_code // 100 != 2:
            raise ValueError("Could not download PGP signature for report: {}.".format(resp.status_code))

        self.logger.info("PGP signature downloaded.")

        # save signature to temporary file
        sign = tempfile.NamedTemporaryFile()
        sign.write(resp.content)
        sign.flush()

        # check signature
        keyring = self.gpg_keyring
        gpg = gnupg.GPG(keyring=keyring)
        verified = gpg.verify_data(sign.name, data)

        # close signature tempfile
        sign.close()

        return verified


BOT = HTTPCollectorBot
