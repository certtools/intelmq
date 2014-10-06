import re
import imbox
import zipfile
from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Report
from intelmq.bots.collectors.mail.lib import Mail

class MailAttachCollectorBot(Bot):

    def process(self):
        mailbox = imbox.Imbox(self.parameters.mail_host, self.parameters.mail_user, self.parameters.mail_password, self.parameters.mail_ssl)
        emails = mailbox.messages(folder=self.parameters.folder, unread=True)

        if emails:
            for uid, message in emails:

                if self.parameters.subject_regex and not re.search(self.parameters.subject_regex, message.subject):
                    continue

                self.logger.info("Reading email report")
                
                for attach in message.attachments:
                    if not attach:
                        continue
                    
                    attach_name = attach['filename'][1:len(attach['filename'])-1] # remove quote marks from filename
                    
                    if re.search(self.parameters.attach_regex, attach_name):

                        if self.parameters.attach_unzip:
                            zipped = zipfile.ZipFile(attach['content'])
                            report_content = zipped.read(zipped.namelist()[0])
                        else:
                            report_content = attach['content'].read()
                            
                        report = Report()
                        report.add('content', report_content)
                            
                        self.send_message(report)
                        
                mailbox.mark_seen(uid)
                self.logger.info("Email report read")


if __name__ == "__main__":
    bot = MailAttachCollectorBot(sys.argv[1])
    bot.start()
