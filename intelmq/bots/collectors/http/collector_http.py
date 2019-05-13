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
"""
import io
import zipfile
from datetime import datetime, timedelta

from intelmq.lib.bot import CollectorBot
from intelmq.lib.utils import unzip

try:
    import requests
except ImportError:
    requests = None


class Time(object):
    def __init__(self, delta=None):
        """ Delta is a datetime.timedelta JSON string, ex: '{days=-1}'. """
        self.time = datetime.now()
        if not isinstance(delta, bool):
            self.time += timedelta(**delta)

    def __getitem__(self, timeformat):
        return self.time.strftime(timeformat)


class HTTPCollectorBot(CollectorBot):

    def init(self):
        if requests is None:
            raise ValueError('Could not import requests. Please install it.')

        self.set_request_parameters()
        self.extract_files = getattr(self.parameters, "extract_files", None)

    def process(self):

        formatting = getattr(self.parameters, 'http_url_formatting', False)
        if formatting:
            try:
                http_url = self.parameters.http_url.format(time=Time(formatting))
            except TypeError:
                self.logger.error("Wrongly formatted http_url_formatting parameter: %s. Should be boolean or a time-delta JSON.",
                                  formatting)
                raise
            except KeyError:
                self.logger.error("Wrongly formatted http_url parameter: %s. Possible misspell with 'time' variable.",
                                  self.parameters.http_url)
                raise
        else:
            http_url = self.parameters.http_url

        self.logger.info("Downloading report from %r.", http_url)

        timeoutretries = 0
        resp = None

        while timeoutretries < self.http_timeout_max_tries and resp is None:
            try:
                resp = requests.get(url=http_url, auth=self.auth,
                                    proxies=self.proxy, headers=self.http_header,
                                    verify=self.http_verify_cert,
                                    cert=self.ssl_client_cert,
                                    timeout=self.http_timeout_sec)

            except requests.exceptions.Timeout:
                timeoutretries += 1
                self.logger.warn("Timeout whilst downloading the report.")

        if resp is None and timeoutretries >= self.http_timeout_max_tries:
            self.logger.error("Request timed out %i times in a row.",
                              timeoutretries)
            return

        if resp.status_code // 100 != 2:
            raise ValueError('HTTP response status code was %i.' % resp.status_code)

        self.logger.info("Report downloaded.")

        raw_reports = []
        try:
            zfp = zipfile.ZipFile(io.BytesIO(resp.content), "r")
        except zipfile.BadZipfile:
            raw_reports.append(resp.text)
        else:
            self.logger.info('Extracting files:'
                             "'%s'.", "', '".join(zfp.namelist()))
            for filename in zfp.namelist():
                raw_reports.append(zfp.read(filename))

        if self.extract_files:
            if isinstance(self.extract_files, str) and len(self.extract_files):
                self.extract_files = self.extract_files.split(",")
                self.logger.info('Extracting files from archive: '
                                 "'%s'.", "', '".join(self.extract_files))
            else:
                self.logger.info('Extracting all files from archive.')
            raw_reports = [file for file in unzip(resp.content, self.extract_files)]

        for raw_report in raw_reports:
            report = self.new_report()
            report.add("raw", raw_report)
            report.add("feed.url", http_url)
            self.send_message(report)


BOT = HTTPCollectorBot
