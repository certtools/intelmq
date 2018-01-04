
With this bot, we are able to send e-mails.

output_gather.py
================
Standard intelmq bot; has got custom output queue. It aggregates the events for later use.

output_send.py
==============
Disabled intelmq bot. Its functionality gets launched by cli.
It loads the events gathered by output_gather.py and sends them to abuse contact e-mails.

Launch it like that:
`</usr/local/bin executable> <bot-id> cli [--tester tester's email]`
Ex:
`intelmq.bots.outputs.mail.output_send  mailsend-output-cz cli --tester edvard.rejthar+test@nic.cz`

Other flags:
```
  -h, --help            show this help message and exit
  --tester TESTING_TO   tester's e-mail
  --ignore-older-than-days IGNORE_OLDER_THAN_DAYS
                        1..n skip all events with time.observation older than
                        1..n day; 0 disabled (allow all)
  --gpgkey GPGKEY       fingerprint of gpg key to be used
  --limit-results LIMIT_RESULTS
                        Just send first N mails.
```

It shows ready e-mails and let you send them to tester's e-mail OR to the recipients.
When done, e-mails are deleted.
E-mails are send in zipped csv file, delimited by comma, strings in "".

The field "raw" gets base64 decoded if possible. Bytes \n and \r are replaced with "\n" and "\r" strings in order to guarantee best CSV files readability both in Office and LibreOffice. A multiline string may be stored in "raw" which completely confused Microsoft Excel.


Configuration:
```json
"alternative_mails": "", # empty string or or path to csv in the form original@email.com,alternative@email.com
"bcc": [], # the list of e-mails to be put in the bcc field for every mail
"emailFrom": "", # sender's e-mail
"gpgkey": "key fingerprint", # (OPTIONAL) fingerprint of a GPG key stored in ~/.gnupg keyring folder
"gpgpass": "password", # (OPTIONAL) password for the GPG key
"mail_template": "", # file containing the body of the mail
"ignore_older_than_days": 0, # (OPTIONAL) 1..n skip all events with time.observation older than 1..n day; 0 disabled (allow all)
"limit_results": 10, # (OPTIONAL) intended as a debugging option, allows loading just first N e-mails from the queue
"redis_cache_db": "",
"redis_cache_host": "",
"redis_cache_port": "",
"redis_cache_ttl": "",
"smtp_server": "mailer",
"subject": "Subject may contain date formatting like this %Y-%m-%d",
"testing_to": "" # (OPTIONAL) default tester's e-mail
```
