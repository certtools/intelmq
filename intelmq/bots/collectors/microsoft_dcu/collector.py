from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.bots import utils

from azure.storage import BlobService

import gzip
import StringIO
import datetime

from urlparse import urlparse


class DCUCollectorBot(Bot):
    """ 
      This IntelMQ collector is for getting a blob
      from an azure account (Microsoft dcu).
      It opens the account and reads all containers.
    """

    def process(self):
        account_name = self.parameters.azure_account_name
        account_key = self.parameters.azure_account_key

        blob_service = BlobService(account_name, account_key, protocol="https")
        proxy_setting = self.parameters.https_proxy or ""
        date_setting = self.parameters.date or ""
        date = None
    
        if date_setting:
            if date_setting != "yesterday":
                date = datetime.datetime.strptime(date_setting, "%Y-%m-%d").date()  # for debbuging (probably)
            elif date_setting == "yesterday":
                date = datetime.date.today() - datetime.timedelta(days=1)  # for normal usage

        proxy_url = "https://" + proxy_setting if proxy_setting.find("https://") == -1 else proxy_setting
        proxy_options = urlparse(proxy_url)

        if date:
            self.logger.info("Fetching for date: %s (%s)" %  (date, date_setting))
        else:
            self.logger.info("No 'date' was specified, fetching ALL")
        
        if proxy_options.hostname:
            self.logger.info("Using https proxy(host=%s, port=%s)" % (proxy_options.hostname, proxy_options.port))
            blob_service.set_proxy(host=proxy_options.hostname, port=proxy_options.port)
        else:
            if proxy_setting:
                self.logger.info("Using NO proxy, couldn't use 'https_proxy' it was: %s" % proxy_setting)
            else:
                self.logger.info("Using NO proxy, 'https_proxy' was empty")

        for container in blob_service.list_containers():
            container_name = container.name
            if container_name == "heartbeat":
                continue

            if date and (not container_name == "processed-" + str(date)):
                self.logger.info("IGNORING container '%s' didn't match date selection" % container_name)
                continue

            for blob in blob_service.list_blobs(container_name):
                self.logger.info("Fetching blob %s in container %s" % (container_name, blob.name))
                data = blob_service.get_blob(container_name, blob.name)
                cs = StringIO.StringIO(data)
                report = gzip.GzipFile(fileobj=cs).read()

                self.send_message(report)

if __name__ == "__main__":
    bot = DCUCollectorBot(sys.argv[1])
    bot.start()
