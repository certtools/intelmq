# -*- coding: utf-8 -*-
"""
FTP collector bot

Parameters:
ftp_host: string
ftp_port: number
ftp_username, ftp_password: string
ftp_directory: string
ftp_file: string

"""
from __future__ import unicode_literals

import fnmatch
import io
import zipfile
from ftplib import FTP

from intelmq.lib.bot import CollectorBot


class FTPCollectorBot(CollectorBot):
    def process(self):
        self.logger.info("Downloading report from %s." %
                         (self.parameters.ftp_host + ':' +
                          str(self.parameters.ftp_port)))

        ftp = FTP()
        ftp.connect(host=self.parameters.ftp_host,
                    port=self.parameters.ftp_port)
        if hasattr(self.parameters, 'ftp_username') \
                and hasattr(self.parameters, 'ftp_password'):
            ftp.login(user=self.parameters.ftp_username,
                      passwd=self.parameters.ftp_password)
        cwd = '/'
        if hasattr(self.parameters, 'ftp_directory'):
            self.logger.debug('Changing working directory to: %r.'
                              '' % self.parameters.ftp_directory)
            cwd = self.parameters.ftp_directory
        ftp.cwd(cwd)

        filemask = '*'
        if hasattr(self.parameters, 'ftp_file'):
            self.logger.debug('Setting filemask to to: %r.'
                              '' % self.parameters.ftp_file)
            filemask = self.parameters.ftp_file

        mem = io.BytesIO()
        files = fnmatch.filter(ftp.nlst(), filemask)

        if files:
            self.logger.info('Retrieving file: %r.' % files[-1])
            ftp.retrbinary("RETR " + files[-1], mem.write)
        else:
            self.logger.info("No file found, terminating download.")
            return

        self.logger.debug("Report downloaded.")

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
            report.add("feed.url", 'ftp://' + self.parameters.ftp_host + ':' +
                       str(self.parameters.ftp_port))
            self.send_message(report)


BOT = FTPCollectorBot
