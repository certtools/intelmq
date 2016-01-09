# -*- coding: utf-8 -*-
"""
FTPS collector bot

Parameters:
ftps_host: string
ftps_port: number
ftps_username, http_password: string
ftps_proxy, http_ssl_proxy: string
ftps_directory: string
ftps_file: string


"""
from __future__ import unicode_literals
import sys
from ftplib import FTP_TLS
import socket
import ssl
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

from intelmq.lib.bot import Bot
from intelmq.lib.harmonization import DateTime
from intelmq.lib.message import Report


# https://stackoverflow.com/questions/12164470/python-ftp-implicit-tls-connection-issue
class FTPS(FTP_TLS):
    def __init__(self, host='', user='', passwd='', acct='', keyfile=None,
                 certfile=None, timeout=60):
        FTP_TLS.__init__(self, host, user, passwd, acct, keyfile, certfile,
                         timeout)

    def connect(self, host='', port=0, timeout=-999):
        if host != '':
            self.host = host
        if port > 0:
            self.port = port
        if timeout != -999:
            self.timeout = timeout

        try:
            self.sock = socket.create_connection((self.host, self.port),
                                                 self.timeout)
            self.af = self.sock.family
            self.sock = ssl.wrap_socket(self.sock, self.keyfile, self.certfile,
                                        ssl_version=ssl.PROTOCOL_TLSv1)
            self.file = self.sock.makefile('rb')
            self.welcome = self.getresp()
        except Exception as e:
            print e
        return self.welcome


class FTPSCollectorBot(Bot):
    def process(self):
        self.logger.info("Downloading report from %s" %
                         self.parameters.ftps_host + ':' +
                         str(self.parameters.ftps_port))

        ftps = FTPS()
        ftps.connect(host=self.parameters.ftps_host,
                     port=self.parameters.ftps_port)
        if hasattr(self.parameters, 'ftps_username') \
                and hasattr(self.parameters, 'ftps_password'):
            ftps.login(user=self.parameters.ftps_username,
                       passwd=self.parameters.ftps_password)
        ftps.prot_p()
        if hasattr(self.parameters, 'ftps_directory'):
            ftps.cwd(self.parameters.ftps_directory)
        mem = StringIO()
        ftps.retrbinary("RETR " + self.parameters.ftps_file, mem.write)

        self.logger.info("Report downloaded.")

        raw_reports = []
        try:
            zfp = zipfile.ZipFile(mem, "r")
        except zipfile.BadZipfile:
            raw_reports.append(mem.getvalue())
        else:
            self.logger.info('Downloaded zip file, extracting following files: '
                             + ', '.join(zfp.namelist()))
            for filename in zfp.namelist():
                raw_reports.append(zfp.read(filename))

        for raw_report in raw_reports:
            report = Report()
            report.add("raw", raw_report, sanitize=True)
            report.add("feed.name", self.parameters.feed, sanitize=True)
            report.add("feed.url", self.parameters.ftps_host + ':' +
                       str(self.parameters.ftps_port), sanitize=True)
            report.add("feed.accuracy", self.parameters.accuracy, sanitize=True)
            time_observation = DateTime().generate_datetime_now()
            report.add('time.observation', time_observation, sanitize=True)
            self.send_message(report)

if __name__ == "__main__":
    bot = FTPSCollectorBot(sys.argv[1])
    bot.start()
