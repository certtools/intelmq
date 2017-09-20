import tarfile
import urllib.request
import urllib.error
import os

from intelmq.lib.bot import CollectorBot

'''
Parameters:
collection: string; collection that should be downloaded.
files: string; file you want to send, for multiple files separate each by ,
'''


class Ut1CollectorBot(CollectorBot):
    def process(self):
        url = "ftp://ftp.ut-capitole.fr/pub/reseau/cache/squidguard_contrib/{}.tar.gz".format(
            self.parameters.collection)
        temp_file = "{}.tar.gz".format(self.parameters.collection)

        self.logger.info("Downloading report from {}".format(url))

        try:
            urllib.request.urlretrieve(url, temp_file)
        except urllib.error.HTTPError as http_e:
            self.logger.info("HTTP error encountered with code {}".format(http_e.code))
        except urllib.error.URLError as url_e:
            self.logger.info("Error encountered {}".format(url_e))
        else:
            self.logger.info("Report downloaded.")

        raw_report = []
        files = self.parameters.files.split(",")
        try:
            tar = tarfile.open(temp_file)
        except tarfile.TarError as tar_e:
            self.logger.info("Error with tar file {}".format(tar_e))
        else:
            for member in tar.getmembers():
                if member.name.split("/")[-1] in files:
                    file = tar.extractfile(member)
                    raw_report.append(file.read())
            tar.close()
            for file in raw_report:
                report = self.new_report()
                report.add("raw", file)
                report.add("feed.url", "https://dsi.ut-capitole.fr/blacklists/{}".format(self.parameters.collection))
                self.send_message(report)

            os.remove(temp_file)


BOT = Ut1CollectorBot
