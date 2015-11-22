import csv
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from intelmq.lib.bot import Bot
from intelmq.lib.cache import Cache
from intelmq.lib.message import Event
import json
import logging
import os
import smtplib
import sys
import time
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

class MailSendOutputBot(Bot):
    def process(self):
        pass

    def init(self):
        self.cache = Cache(
                           self.parameters.redis_cache_host,
                           self.parameters.redis_cache_port,
                           self.parameters.redis_cache_db,
                           self.parameters.redis_cache_ttl
                           )
        self.send_mails()

    # Posle vsechny maily
    def send_mails(self):
        self.logger.warning("Going to send mails...")
        with open(self.parameters.mail_template) as f:
            mailContents = f.read()

        for mail_record in self.cache.redis.keys("mail:*"):
            self.logger.warning("Next:")
            self.logger.warning("Mail", mail_record)
            lines = []
            self.logger.debug(mail_record)
            for message in self.cache.redis.lrange(mail_record, 0, -1):
                lines.append(json.loads(unicode(message))) # lines.append(unicode(message))

            fieldnames = set()
            for row in lines:
                fieldnames = fieldnames | set(row.keys())
            output = StringIO()
            dict_writer = csv.DictWriter(output, fieldnames=fieldnames)
            dict_writer.writerow(dict(zip(fieldnames, fieldnames)))
            dict_writer.writerows(lines)

            self._send_mail(self.parameters.emailFrom, mail_record[len("mail:"):], "Threat list", mailContents, output.getvalue()) #"\n".join(lines)
            self.cache.redis.delete(mail_record)
        self.logger.warning("DONE!")


    def _send_mail(self, emailfrom, emailto, subject, text, fileContents=None, server="127.0.0.1"):
        msg = MIMEMultipart()
        msg["From"] = emailfrom
        msg["Subject"] = subject + " " + emailto #XXX dat pryc emailto
        msg["To"] = "edvard.rejthar+test_output@nic.cz" # XXX emailto
        
        msg.attach(MIMEText(text, "plain", "utf-8"))


        maintype, subtype = "text/json".split("/", 1) # XXX ma to posilat CSV, ne JSON. Ale nemaji jednotlive messages ruzne sloupecky (kazdy jiny pocet sloupecku z taxonomie)?
        if maintype == "text":
            attachment = MIMEText(fileContents, _subtype=subtype)
        attachment.add_header("Content-Disposition", "attachment", filename='list_{}.csv'.format(time.strftime("%Y%m%d")))
        msg.attach(attachment)

        smtp = smtplib.SMTP(server)
        smtp.sendmail(emailfrom, "edvard.rejthar+test_output@nic.cz", msg.as_string().encode('ascii')) # XXXX emailto
        smtp.close()



if __name__ == "__main__":
    bot = MailSendOutputBot(sys.argv[1])
    bot.start()