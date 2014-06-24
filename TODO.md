## Release 1 - TODO

(sorted by priority)

* Support multiple destination queues for each bot

* ContactDB Expert (Install ContactDB)
    
* MailBox
    * split by specific keys
    * template(subject/message) configurable with variables
    * use 'abuse contact' field to ge the email to send ('abuse contact' was filled by ContactDB)
    * STIX Format
    * IODEF Format
    * CSV Format
    * Events that MailBox will send must be stored in a specific Database to get again all events if mailer crash or wtv
    * In the end MailBox must send a summary of sent reports
    * RTIR Output Bot
    
* Trash Queue when bot do not recognize the message and cant do nothing

* Quality Control: perfomance tests, security configurations and queues snapshoting
    * Queue Durability / Persistente Messages (search for 'Queue Durability'): http://www.rabbitmq.com/tutorials/amqp-concepts.html

* Documentation

* ElasticSearch Output Bot

* Video Tutorial

* General Bots Configuration (DONE -> bots access the parameters via self.parameters.parameter_name, name can be easily changed)  **[DONE]**
* 
* AbuseHelper Integration  **[DONE -> xmpp bot to connect to room]**

* Splunk Output Bot  **[DONE]**

* TeamCymru Expert  **[DONE]**

## Release 2 - TODO

* HPFeeds/Frieds like system to manage who has access to the feeds etc...

* Use the IFAS Report Interface for MailBox

* Change to Python3 ?

* The pipeline send and receive for events is very ugly. Put it better

* 1-N queues problem
    * support multiple queues as destination
    * current solution just behave like a HUB and should behave like a Router.

* Pipeline Management (Web Interface)

* JSON Messages
    * with tag field (report, abuse-event, pastebin, tweet)
    * with syntax abusehelper event-like ( event.add("domain", "example.com") )
    * __hash__ method

* PostgreSQL (Reports, Events)

* Bots to create:
    * Cymru
    * MaxMind GeoIP
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
    * [VXVault](https://bitbucket.org/slingris/abusehelper/src/d5a32b813593/abusehelper/contrib/vxvault/?at=default)
    * [XSSed](https://bitbucket.org/slingris/abusehelper/src/d5a32b813593/abusehelper/contrib/xssed/?at=default)

## Feedback

### Chris Horsley Feedback

| Requirement | Reason | Possible Solutions |
|---|-----------------------------------------|------------------------------------------------------------|---|---|
| Can use lightweight threads | Minimal overhead for memory | http://gevent.org/ , https://pypi.python.org/pypi/greenlet |
| Can run distributed over network | Redundancy of system, may want to process event data on separate machine do data storage one day | http://python-rq.org/ , http://www.celeryproject.org/ , https://github.com/pika/pika |
| Can support a sequential processing pipeline | Need an API to schedule and execute remote data processing functions in order | http://www.celeryproject.org/ , Custom API |
| Can process events in parallel | Avoids slow, serial processing of a long series of events, parallel processing gives large speed benefits where there are network / database calls | http://python-rq.org/ http://www.celeryproject.org/ |
| Don't reinvent message serialization / scheduling | Remote function execution is a hard problem to solve (e.g. locking, scheduling), use a library that's well tested and supported | http://python-rq.org/ http://www.celeryproject.org/ |

