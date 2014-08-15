import re
import imbox
import zipfile
from intelmq.lib.bot import Bot, sys
from intelmq.bots.collectors.mail.lib import Mail

class MailAttachCollectorBot(Bot):

    def process(self):
        mailbox = imbox.Imbox(self.parameters.mail_host, self.parameters.mail_user, self.parameters.mail_password, bool(self.parameters.mail_ssl))
        emails = mailbox.messages(folder=self.parameters.folder, unread=True)

        if emails:
            for uid, message in emails:

                if self.parameters.subject_regex and not re.search(self.parameters.subject_regex, message.subject):
                    continue

                self.logger.info("Reading email report")
                
                for attach in message.attachments:
                    if not attach:
                        continue
                    
                    if re.search(self.parameters.attach_regex, attach['filename']):
                        
                        if self.parameters.attach_unzip:
                            zipped = zipfile.ZipFile(attach['content'])
                            report = zipped.read(zipped.namelist()[0])
                        else:
                            report = attach['content']
                            
                        self.send_message(report)
                        
                mailbox.mark_seen(uid)
                self.logger.info("Email report read")


if __name__ == "__main__":
    bot = MailAttachCollectorBot(sys.argv[1])
    bot.start()