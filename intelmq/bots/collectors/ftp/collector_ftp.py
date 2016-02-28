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
import sys
from ftplib import FTP
import socket
import zipfile
import io

from intelmq.lib.bot import Bot
from intelmq.lib.harmonization import DateTime
from intelmq.lib.message import Report


class FTPCollectorBot(Bot):
    def process(self):
        self.logger.info("Downloading report from %s" %
                         self.parameters.ftp_host + ':' +
                         str(self.parameters.ftp_port))

        ftp = FTP()
        ftp.connect(host=self.parameters.ftp_host,
                     port=self.parameters.ftp_port)
        if hasattr(self.parameters, 'ftp_username') \
                and hasattr(self.parameters, 'ftp_password'):
            ftps.login(user=self.parameters.ftp_username,
                       passwd=self.parameters.ftp_password)
        cwd = '/'
        if hasattr(self.parameters, 'ftp_directory'):
            cwd = self.parameters.ftp_directory
        ftp.cwd(cwd)
        mem = io.BytesIO()
        if hasattr(self.parameters, 'ftp_file'):
            ftp.retrbinary("RETR " + self.parameters.ftp_file, mem.write)
        else:
            files = ftp.nlst(cwd)
            if files.count() > 0:
                #retrieve the last file in the directory
                ftp.retrbinary("RETR " + files[-1], mem.write)
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
            self.logger.info('Downloaded zip file, extracting following files: '
                             + ', '.join(zfp.namelist()))
            for filename in zfp.namelist():
                raw_reports.append(zfp.read(filename))

        for raw_report in raw_reports:
            report = Report()
            report.add("raw", raw_report, sanitize=True)
            report.add("feed.name", self.parameters.feed, sanitize=True)
            report.add("feed.url", self.parameters.ftp_host + ':' +
                       str(self.parameters.ftp_port), sanitize=True)
            report.add("feed.accuracy", self.parameters.accuracy, sanitize=True)
            time_observation = DateTime().generate_datetime_now()
            report.add('time.observation', time_observation, sanitize=True)
            self.send_message(report)

if __name__ == "__main__":
    bot = FTPCollectorBot(sys.argv[1])
    bot.start()
