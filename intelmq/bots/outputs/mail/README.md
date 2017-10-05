
 ** THIS FILE IS OLD and should be updated **

Bot „Generate Abuse Emails“ je spouštěn v pravidelných intervalech (zatím jednou denně v 7:00 – bude uvedeno v konfiguraci bota).
Kromě tohoto cyklického spouštění žádné akce nevykonává, pouze se mu plní fronta s novými událostmi.
Běh bota se dělí do dvou velkých fází – Email Aggregation a Send Emails.

První úkol programu bude vytvořit si seznamy událostí se společným adresátem.
Bot se podívá na první událost v bufferu (abuse-mailer-queue) a vytvoří nový seznam pro adresáta z této první události.
Následně „popuje“ všechny události se stejným adresátem do tohoto nového seznamu.
Tento cyklus s vytvořením nového seznamu pro každého unikátního adresáta se opakuje,
    dokud není původní fronta prázdná.
Bot zahazuje všechny události, které vůbec neobsahují abuse kontakt (emailovou adresu), i když by k tomu nemělo dojít.

Druhá fáze již připravuje a odesílá emaily.
Pro každý seznam připravený v předchozí fázi bude vytvořen právě jeden email kombinující klasický text a strojově zpracovatelné přílohy.
Příloha bude csv zahrnující část informací z události v IntelMQ.
Celá akce přípravy emailu musí proběhnout jako transakce odolná proti výpadku:
1. Email je připraven v paměti bota
2. Email je zapsán do nezávislé redis queue (email-template-queue)
3. Seznam událostí použitý pro přípravu emailu je odstraněn
4. Email je odeslán na nakonfigurovaný smtp server (uvedený v konfiguraci bota)

Problém: mají být emaily anglicky nebo česky? Mohou být kombinované html + txt?

Aby byla odolná proti výpadku, vymažu seznam událostí (tj. frontu abuse-mailer-queue ?) asi až potom, co projde příkaz, který posílá zprávu na smtp, tj. body 3 a 4 jsou prohozeny.

Configuration:
"bcc": [], # the list of e-mails to be put in the bcc field for every mail
"emailFrom": "",
"mail_template": "", # file containing the body of the mail
"redis_cache_db": "",
"redis_cache_host": "",
"redis_cache_port": "",
"redis_cache_ttl": "",
"smtp_server": "mailer",
"testing_to": "" # if a value is used, all the mails are sent TO THIS E-MAIL ONLY (with a subject line informing who the mail was intended for originally) and bcc field gets ignored
