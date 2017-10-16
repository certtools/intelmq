
With this bot, we are able to send e-mails.

output_gather.py
================
Standard intelmq bot; has got custom output queue. It aggregates the events for later use.

output_send.py
==============
Disabled intelmq bot. Its functionality gets launched by cli.
It loads the events gathered by output_gather.py and sends them to abuse contact e-mails.

Launch it like that:
</usr/local/bin executable> <bot-id> cli [--tester tester emails]
Ex:
intelmq.bots.outputs.mail.output_send  mailsend-output-cz cli --tester edvard.rejthar+test@nic.cz

It shows ready e-mails and let you send them to tester's e-mail OR to the recipients.
When done, e-mails are deleted.
E-mails are send in zipped csv file, delimited by comma, strings in "".


Configuration:
"alternative_mails": "", # empty string or or path to csv in the form original@email.com,alternative@email.com
"bcc": [], # the list of e-mails to be put in the bcc field for every mail
"emailFrom": "", # sender's e-mail
"mail_template": "", # file containing the body of the mail
"redis_cache_db": "",
"redis_cache_host": "",
"redis_cache_port": "",
"redis_cache_ttl": "",
"smtp_server": "mailer",
"subject": "Subject may contain date formatting like this %Y-%m-%d",
"testing_to": "" # default tester's e-mail
