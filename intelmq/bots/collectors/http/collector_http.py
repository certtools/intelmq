# -*- coding: utf-8 -*-
"""
HTTP collector bot

Parameters:
http_url: string
http_header: dictionary
    default: {}
http_verify_cert: boolean
    default: True
http_username, http_password: string
http_proxy, https_proxy: string
http_timeout_sec: tuple of two floats or float
http_timeout_max_tries: an integer depicting how often a connection attempt is retried
"""
import io
import zipfile

import requests

from intelmq.lib.bot import CollectorBot


class HTTPCollectorBot(CollectorBot):

    def init(self):
        self.set_request_parameters()

    def process(self):
        self.logger.info("Downloading report from %s", self.parameters.http_url)

        timeoutretries = 0
        resp = None

        while timeoutretries < self.http_timeout_max_tries and resp is None:
            try:
                resp = requests.get(url=self.parameters.http_url, auth=self.auth,
                                    proxies=self.proxy, headers=self.http_header,
                                    verify=self.http_verify_cert,
                                    cert=self.ssl_client_cert,
                                    timeout=self.http_timeout_sec)

            except requests.exceptions.Timeout:
                timeoutretries += 1
                self.logger.warn("Timeout whilst downloading the report.")

        if resp is None and timeoutretries >= self.http_timeout_max_tries:
            self.logger.error("Request timed out %i times in a row. " %
                              timeoutretries)
            return

        if resp.status_code // 100 != 2:
            raise ValueError('HTTP response status code was {}.'
                             ''.format(resp.status_code))

        self.logger.info("Report downloaded.")

        raw_reports = []
        try:
            zfp = zipfile.ZipFile(io.BytesIO(resp.content), "r")
        except zipfile.BadZipfile:
            raw_reports.append(resp.text)
        else:
            self.logger.info('Downloaded zip file, extracting following files:'
                             ' ' + ', '.join(zfp.namelist()))
            for filename in zfp.namelist():
                raw_reports.append(zfp.read(filename))

        for raw_report in raw_reports:
            report = self.new_report()
            report.add("raw", raw_report)
            report.add("feed.url", self.parameters.http_url)
            self.send_message(report)


BOT = HTTPCollectorBot
