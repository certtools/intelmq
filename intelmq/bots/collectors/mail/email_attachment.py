from intelmq.lib.bot import Bot, sys
from intelmq.lib.utils import fetch_imap

class EmailAttachmentCollectorBot(Bot):

    def process(self):
        
        # TODO: accept multiple attachment names
                
        additional_parameters = ["folder", "unread", "sent_from", "sent_to", "subject", "max_emails"]
        
        for param in additional_parameters:
            if not hasattr(self.parameters, param):
                setattr(self.parameters, param, None)
        
        emails = fetch_imap(self.parameters.host,
                            self.parameters.user,
                            self.parameters.password,
                            self.parameters.ssl,
                            self.parameters.attach
                            self.parameters.folder,
                            self.parameters.unread,
                            self.parameters.sent_from,
                            self.parameters.sent_to,
                            self.parameters.subject,
                            self.parameters.max_emails,
                           )
                            
        for email in emails:
            for attach in message.attachments:
                self.parameters.attach = '"%s"' % self.parameters.attach
                if self.parameters.attach == attach['filename']:
                    report = u"".join(attach['content'].read())
    
                self.send_message(report)


if __name__ == "__main__":
    bot = EmailAttachmentCollectorBot(sys.argv[1])
    bot.start()
