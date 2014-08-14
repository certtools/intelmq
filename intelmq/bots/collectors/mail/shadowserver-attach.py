import imbox
import zipfile
from intelmq.lib.bot import Bot, sys
from intelmq.bots.collectors.mail.lib import Mail

class ShadowServerCollectorBot(Bot):

    def process(self):
        additional_parameters = ["folder", "unread", "sent_from", "subject_regex", "attach_regex"]
        
        for param in additional_parameters:
            if not hasattr(self.parameters, param):
                setattr(self.parameters, param, None)

        mailbox = imbox.Imbox(self.parameters.mail_host, self.parameters.mail_user, self.parameters.mail_password, bool(self.parameters.mail_ssl))
        emails = mailbox.messages(folder=self.parameters.folder, unread=self.parameters.unread, sent_from=self.parameters.sent_from)

        if emails:
            for uid, message in emails:

                if self.parameters.subject_regex and not self.parameters.subject_regex in message.subject: # Apply regex
                    continue
                
                for attach in message.attachments:
                    if not attach:
                        continue
                    
                    if self.parameters.attach_regex in attach['filename']: # Apply regex
                        
                        zipped = zipfile.ZipFile(attach['content'])
                        report_csv = zipped.read(zipped.namelist()[0])
                        
                        #report_link = "# Feed: http://dl.shadowserver.org/CHANGEME" # URL (dl.shadowserver.org/) regex apllied to message.body['plain'] or message.body['html']
                        report = report_csv # report_link + report_csv
                        self.send_message(report)
                        
                mailbox.mark_seen(uid)


if __name__ == "__main__":
    bot = ShadowServerCollectorBot(sys.argv[1])
    bot.start()
