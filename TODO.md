## Release 1 - TODO

(sorted by priority)

* https://github.com/nicolasff/phpredis

* Create n6 bot.

* Create [Shadowserver Bots](http://www.shadowserver.org/wiki/pmwiki.php/Services/Downloads)

* Create [Malware Hash Registry - Cymru](http://www.team-cymru.org/Services/MHR/#dns)

* Write docs/eCSIRT-Taxonomy.md based on document from Don Stikvoort, named "Incident Class mkVint"

* Check [RabbitMQ based fork of CIF v1](https://github.com/cikl), [Warden](https://csirt.cesnet.cz/Warden/Intro) and [Build STIX document from CIF output](http://tools.netsa.cert.org/script-cif2stix/index.html)

* **[DONE]** General Bots Configuration (bots access the parameters via self.parameters.parameter_name, name can be easily changed)

* **[DONE]** AbuseHelper Integration (xmpp bot to connect to room)

* **[DONE]** Splunk Output Bot

* **[DONE]** TeamCymru Expert

* **[DONE]** Support multiple destination queues for each bot

* **[DONE]** Write Bot Architecture (event, cache, utils relations etc...)

* **[DONE]** Remove Cache initiallization from bot.py. Create a 'init' method to all class that ineherit from bot.py.

* **[DONE]** Remove all self.parameters from bot.py

* **[DONE]** Create configuration option for logs folder (change in bot.py)

* **[DONE]** Add in each expert a line to test if the augment keys already exists

* **[DONE]** Remove "observation time" for event in deduplicator bot

* **[DONE]** Quality Control: perfomance tests

* **[DONE]** Create a python package and use this setup.py [example](https://github.com/pika/pika/blob/master/setup.py)

## Release 2 - TODO

* Create RabbitMQ queue for bot management and state sharing

* Create bots for all feeds that are not available in AbuseHelper (INTECO, CERT-EU, etc)

* New bots: https://github.com/collectiveintel/cif-v1/tree/686c9ac9c34658ccc83d5b9fea97972eeaad0f29/cif-smrt/rules/etc

* Improve encoding/decoding

* Add 'requirements.txt' with fixed version numbers for each package -> pip install -r requirements.txt

* Remove old queues depending of load configuration

* Restruct repository and may be create python packages:
```
/src
  /intellib  -> /usr/local/lib/python.....
  /intelmq   -> /opt/
     /bots
     /confs
/docs
..files...
```

* ElasticSearch Output Bot

* Evaluate how to initiallize bots from command-line: /etc/init.d/arbor-feed start ??? Or just with webinterface?

* ContactDB Expert (Install ContactDB)

* Trash Queue when bot do not recognize the message and cant do nothing

* Create a management interface to give feed access to other people. Good example: HPFrieds/HPFeeds system.

* Evaluate: Python 3 vs Python 2.7

* 1-N Queues: support other exchange types (current solution support fanout)

* Pipeline Management with Web Interface

* Bots Management with Web Interface

* Video Tutorial
 
* Monitoring with Web Interface

* JSON Messages
    * with tag field (report, abuse-event, pastebin, tweet)
    * with syntax abusehelper event-like ( event.add("domain", "example.com") )
    * __hash__ method
    * evaluate: http://danielmiessler.com/study/url_vs_uri/

* PostgreSQL (Reports, Events)

* Bots to create:
    * MalwareHash
    * RT
    * SSHKeyScan
    * URL2Domain
    * isOutCustomer
    * CrowdStrike
    * DomainTools
    * VirusTotal
    * Shodan
    * PassiveDNS
    * [HostFiles](https://bitbucket.org/slingris/abusehelper/src/d5a32b813593/abusehelper/contrib/hostfiles/?at=default)
    * [MalwarePatrol](https://bitbucket.org/slingris/abusehelper/src/d5a32b813593/abusehelper/contrib/malwarepatrol/?at=default)
    * [n6](https://bitbucket.org/slingris/abusehelper/src/d5a32b813593/abusehelper/contrib/n6/?at=default)
    * [OpenBL](https://bitbucket.org/slingris/abusehelper/src/d5a32b813593/abusehelper/contrib/openbl/?at=default)
    * [SQLBot](https://bitbucket.org/slingris/abusehelper/src/d5a32b813593/abusehelper/contrib/sqlbot/?at=default)
    * [XSSed](https://bitbucket.org/slingris/abusehelper/src/d5a32b813593/abusehelper/contrib/xssed/?at=default)
    * **[DONE]** [VXVault](https://bitbucket.org/slingris/abusehelper/src/d5a32b813593/abusehelper/contrib/vxvault/?at=default)

## Feedback

### Chris Horsley Feedback

| Requirement | Reason | Possible Solutions |
|---|-----------------------------------------|------------------------------------------------------------|---|---|
| Can use lightweight threads | Minimal overhead for memory | http://gevent.org/ , https://pypi.python.org/pypi/greenlet |
| Can run distributed over network | Redundancy of system, may want to process event data on separate machine do data storage one day | http://python-rq.org/ , http://www.celeryproject.org/ , https://github.com/pika/pika |
| Can support a sequential processing pipeline | Need an API to schedule and execute remote data processing functions in order | http://www.celeryproject.org/ , Custom API |
| Can process events in parallel | Avoids slow, serial processing of a long series of events, parallel processing gives large speed benefits where there are network / database calls | http://python-rq.org/ http://www.celeryproject.org/ |
| Don't reinvent message serialization / scheduling | Remote function execution is a hard problem to solve (e.g. locking, scheduling), use a library that's well tested and supported | http://python-rq.org/ http://www.celeryproject.org/ |

