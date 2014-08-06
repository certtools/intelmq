from intelmq.lib.bot import Bot, sys
from intelmq.lib.utils import fetch_imap
import zipfile

class EmailAttachmentCollectorBot(Bot):

    def process(self):
                
        additional_parameters = ["folder", "unread", "sent_from", "sent_to", "subject", "max_emails"]
        
        for param in additional_parameters:
            if not hasattr(self.parameters, param):
                setattr(self.parameters, param, None)
        
        emails = fetch_imap(self.parameters.host,
                            self.parameters.user,
                            self.parameters.password,
                            self.parameters.ssl,
                            self.parameters.folder,
                            self.parameters.unread,
                            self.parameters.sent_from,
                            self.parameters.sent_to,
                            self.parameters.subject,
                            self.parameters.max_emails,
                           )
        
        for email in emails:
            for attach in email.attachments:
                if attach:
                    if self.parameters.attach in attach['filename']:
                        if unzip:
                            zipped = zipfile.ZipFile(attach['content'])
                            for name in zipped.namelist():
                                report = zipped.read(name)
                                self.send_message(report)
                        else:
                            report = attach['content'].read()
                            self.send_message(report)

# TODO: subject needs to be regex
# TODO: attachments needs to be regex
# TODO: accept multiple attachment names

if __name__ == "__main__":
    bot = EmailAttachmentCollectorBot(sys.argv[1])
    bot.start()
