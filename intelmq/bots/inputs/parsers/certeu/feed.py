import sys
from intelmq.lib.bot import *
from intelmq.lib.utils import *
from intelmq.lib.event import *
from imbox import Imbox
import traceback

### Begin * Testing purposes
fp = open("/tmp/password.txt", 'r')
PASSWORD = fp.read().strip()
fp.close()
### End


class CERTEUFeedBot(Bot): 
    def process(self):
        mailbox = Imbox('imap.fccn.pt',
                        username = 'abuse-feeds-test', 
                        password = PASSWORD,
                        ssl = True
                    )
        
        messages_folder = mailbox.messages(
                            folder='Inbox.cert-eu',
                            unread=True
                            )
        
        subject_regex = "Summary of your"

        for uid, message in messages_folder:
            if subject_regex in message.subject:
                for attach in message.attachments:
                    if '"report.csv"' == attach['filename']:
                        report = u"".join(attach['content'].read())
                        
                        print "Report is: %s with %d" % (report, report.count('\n'))
                        if report:
                            self.logger.info('Push report to queue')
                            self.send_message(report)
                        else:
                            self.logger.info('Empty report')                        
                        
                        #mailbox.mark_seen(uid)







if __name__ == "__main__":
    bot = CERTEUFeedBot(sys.argv[1])
    bot.start()
