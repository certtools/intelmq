import re
import imbox
import zipfile
from intelmq.lib.bot import Bot, sys
from intelmq.bots.collectors.mail.lib import Mail
from intelmq.bots.collectors.url.lib import fetch_url

class ShadowServerURLCollectorBot(Bot):

    def process(self):
        additional_parameters = ["folder", "unread", "sent_from", "subject_regex", "url_regex"]
        
        for param in additional_parameters:
            if not hasattr(self.parameters, param):
                setattr(self.parameters, param, None)

        mailbox = imbox.Imbox(self.parameters.mail_host, self.parameters.mail_user, self.parameters.mail_password, bool(self.parameters.mail_ssl))
        emails = mailbox.messages(folder=self.parameters.folder, unread=self.parameters.unread, sent_from=self.parameters.sent_from)

        if emails:
            for uid, message in emails:
                
                for body in message.body['plain']:
                    match = re.search(self.parameters.url_regex, body)
                    if match:
                        url = match.group()
                        
                        self.logger.info("Downloading report from %s" % url)
                        report = fetch_url(url, timeout = 60.0, chunk_size = 16384)
                        self.logger.info("Report downloaded.")
                        
                        self.send_message(report)
                        
                mailbox.mark_seen(uid)


if __name__ == "__main__":
    bot = ShadowServerURLCollectorBot(sys.argv[1])
    bot.start()
