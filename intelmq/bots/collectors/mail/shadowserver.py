# TODO: subject needs to be regex
# TODO: attachments needs to be regex
# TODO: accept multiple attachment names
# TODO: add method to mark email as read

from intelmq.lib.bot import Bot, sys
from intelmq.bots.collectors.mail.lib import Mail
import zipfile

# Fields Required:
# ---------------------
# * mail_host - imap server
# * mail_user - user of email account
# * mail_password - password of email account
# * mail_ssl - use secure connenctions (True/False)
# * folder - email folder (e.g. Inbox.ShadowServer)
# * unread - get just unread emails (True/False)
# * sent_from - source email from message that was sent
# * subject_regex - subject of the message
# * attach_regex - name of the attach to fetch
# * unzip - unzip attach (True/False)

class ShadowServerCollectorBot(Bot):

    def process(self):
        additional_parameters = ["folder", "unread", "sent_from", "subject_regex", "attach_regex"]
        
        for param in additional_parameters:
            if not hasattr(self.parameters, param):
                setattr(self.parameters, param, None)

        mailbox = imbox.Imbox(self.parameters.mail_host, self.parameters.mail_user, self.parameters.mail_password, bool(self.parameters.mail_ssl))
        uid, message = mailbox.messages(folder=self.parameters.folder, unread=self.parameters.unread, sent_from=self.parameters.sent_from)

        if uid:
            if self.parameters.subject_regex and not self.parameters.subject_regex in message.subject: # Apply regex
                return
            
            for attach in message.attachments:
                if self.parameters.attach_regex in attach['filename']: # Apply regex
                    
                    zipped = zipfile.ZipFile(attach['content'])
                    report_csv = zipped.read(zipped.namelist()[0])
                    
                    report_link = "# Feed: http://dl.shadowserver.org/CHANGEME" # URL (dl.shadowserver.org/) regex apllied to message.body['plain'] or message.body['html']
                    report = report_link + report_csv
                    
                    self.send_message(report)
                    mailbox.mark_seen(uid)


if __name__ == "__main__":
    bot = ShadowServerCollectorBot(sys.argv[1])
    bot.start()
