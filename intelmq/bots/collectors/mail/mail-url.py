import re
import imbox
from intelmq.lib.bot import Bot, sys
from intelmq.bots.collectors.mail.lib import Mail
from intelmq.bots.collectors.url.lib import fetch_url

class MailURLCollectorBot(Bot):

    def process(self):
        mailbox = imbox.Imbox(self.parameters.mail_host, self.parameters.mail_user, self.parameters.mail_password, self.parameters.mail_ssl)
        emails = mailbox.messages(folder=self.parameters.folder, unread=True)

        if emails:
            for uid, message in emails:
                
                if self.parameters.subject_regex and not re.search(self.parameters.subject_regex, message.subject):
                    continue
                
                self.logger.info("Reading email report")
                
                for body in message.body['plain']:
                    match = re.search(self.parameters.url_regex, body)
                    if match:
                        url = match.group()
                        
                        self.logger.info("Downloading report from %s" % url)
                        report = fetch_url(url, timeout = 60.0, chunk_size = 16384)
                        self.logger.info("Report downloaded.")
                        
                        self.send_message(report)
                        
                mailbox.mark_seen(uid)
                self.logger.info("Email report read")


if __name__ == "__main__":
    bot = MailURLCollectorBot(sys.argv[1])
    bot.start()
