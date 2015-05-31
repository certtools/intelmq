Core Priorities:
===============================

1) Add support on IntelMQ-Manager for default section parameters  

2) Harmonization (force flag)- feature which gives possibility to select the keys that will force the fail of the parse and which keys the parse will
ignore and continue the process in case of fail in parse. Example:
		++ If source.ip has some problem, the event should follow the normal procedure of error handling
		++ If source.asn has some problem, since its not an important key, the event can ignore the value and continue the process

3) Any exception in init() method should be fatal. It means that init need to catch every exception and log a messsage like "im stopping" and raise something....

4) check_bot_id should raise an exception like mentioned before

5) Translate current bots

6) Move new bots and translate them

7) Video Tutorial



Other Tasks:
===============================

1) intelmqctl improvements
	- load parameters from all configurations
	- bot.py must has statis methods to load configurations and then intelmqctl will be able to use them


4) some keys like 'source.ip', 'source.domain_name', 'source.url' are really crucial for the event context.
When parse fail becasue the ip collumn from the source has an URL, its hard to have good code to handle this and 
put back the URL from IP collumn to source.url key in event. For this reason, we should create a util that try to guess
what type is the value, but must follow an order:
	- IPAddress check
	- URL check
	- DomainName check

5) Clean up DataHarmonization document - include a default intelmq Event message in JSON format

6)  Update documentation:
	- explain the configuration parameters from bots
	- explain how harmonization.conf file works and how keys are converted in the end to JSON

7) Harmonization:
	- add 'confidence_level' key to Event object (Harmonization)
	- add 'TLP' key to Event object (Harmonization)
	- rename source.email_address to source.account (where you can specify email address and unix/windows accounts, etc...)
	- rename source.url to source.uri (https://danielmiessler.com/study/url_vs_uri/)

12) O feed.url ja devia vir do collector url. O collector automaticamente devia adicionar o url onde vai buscar a informaçao como key, assim como devia adicionar um timestamp de quando foi buscar. Estas a repetir sempre o mesmo em todos os parsers o que nao faz sentido. ALem disso o feed.name tambem devia ser definido no collector, porque é ai que estás a definir onde vais buscar a informação.

13) Add regex (harmonization.conf parameters) check in harmonization.py

14) Redis Configurations should be configured by configurations and not hardcoded

15) Bots
	- CollectorBot - TCPServerSocket
	- PGP support
    - Write docs/eCSIRT-Taxonomy.md based on document from Don Stikvoort, named "Incident Class mkVint"
    - Check [RabbitMQ based fork of CIF v1](https://github.com/cikl), [Warden](https://csirt.cesnet.cz/Warden/Intro) and [Build STIX document from CIF output](http://tools.netsa.cert.org/script-cif2stix/index.html)
    - New bots: https://github.com/collectiveintel/cif-v1/tree/686c9ac9c34658ccc83d5b9fea97972eeaad0f29/cif-smrt/rules/etc
    - ContactDB Expert
    - PostgreSQL (Reports, Events)
    - RT
    - SSHKeyScan
    - isOutCustomer
    - CrowdStrike
    - Shodan
    - PassiveDNS
    - [XSSed](https://bitbucket.org/slingris/abusehelper/src/d5a32b813593/abusehelper/contrib/xssed/?at=default)

16) Python Requirements
    - add 'requirements.txt' with fixed version numbers for each package -> pip install -r requirements.txt

17) Remove old queues procedure
    - remove old queues depending of load configuration
