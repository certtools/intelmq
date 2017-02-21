# -*- coding: utf-8 -*-
"""
FTPS collector bot

Parameters:
ftps_host: string
ftps_port: number
ftps_username, ftps_password: string
ftps_directory: string
ftps_file: string


"""
from __future__ import unicode_literals

import fnmatch
import io
import socket
import ssl
import zipfile
from ftplib import FTP_TLS

from intelmq.lib.bot import CollectorBot


# BEGIN content from Stack Overflow
# cc by-sa 3.0
# Original question: https://stackoverflow.com/questions/12164470/python-ftp-implicit-tls-connection-issue
# Question author (Martin Prikryl): https://stackoverflow.com/users/850848/martin-prikryl
# Answer author (Grzegorz Wierzowiecki): https://stackoverflow.com/users/544721/grzegorz-wierzowiecki
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

        self.sock = socket.create_connection((self.host, self.port),
                                             self.timeout)
        self.af = self.sock.family
        self.sock = ssl.wrap_socket(self.sock, self.keyfile, self.certfile,
                                    ssl_version=ssl.PROTOCOL_TLSv1)
        self.file = self.sock.makefile('rb')
        self.welcome = self.getresp()

        return self.welcome
# END content from Stack Overflow


class FTPSCollectorBot(CollectorBot):
    def process(self):
        self.logger.info("Downloading report from %s." %
                         (self.parameters.ftp_host + ':' +
                          str(self.parameters.ftp_port)))

        ftps = FTPS()
        ftps.connect(host=self.parameters.ftps_host,
                     port=self.parameters.ftps_port)
        if hasattr(self.parameters, 'ftps_username') \
                and hasattr(self.parameters, 'ftps_password'):
            ftps.login(user=self.parameters.ftps_username,
                       passwd=self.parameters.ftps_password)
        ftps.prot_p()

        cwd = '/'
        if hasattr(self.parameters, 'ftps_directory'):
            self.logger.debug('Changing working directory to: %r.'
                              '' % self.parameters.ftp_directory)
            cwd = self.parameters.ftps_directory
        ftps.cwd(cwd)

        filemask = '*'
        if hasattr(self.parameters, 'ftps_file'):
            self.logger.debug('Setting filemask to to: %r.'
                              '' % self.parameters.ftp_file)
            filemask = self.parameters.ftps_file

        mem = io.BytesIO()
        files = fnmatch.filter(ftps.nlst(), filemask)

        if files:
            self.logger.info('Retrieving file: ' + files[-1])
            ftps.retrbinary("RETR " + files[-1], mem.write)
        else:
            self.logger.error("No file found, terminating download")
            return

        self.logger.info("Report downloaded.")

        raw_reports = []
        try:
            zfp = zipfile.ZipFile(mem, "r")
        except zipfile.BadZipfile:
            raw_reports.append(mem.getvalue())
        else:
            self.logger.info('Downloaded zip file, extracting following files: %r'
                             '' % zfp.namelist())
            for filename in zfp.namelist():
                raw_reports.append(zfp.read(filename))

        for raw_report in raw_reports:
            report = self.new_report()
            report.add("raw", raw_report)
            report.add("feed.url", 'ftps://' + self.parameters.ftps_host + ':' +
                       str(self.parameters.ftps_port))
            self.send_message(report)


BOT = FTPSCollectorBot
