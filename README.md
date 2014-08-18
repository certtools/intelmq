# IntelMQ

IntelMQ is a solution for CERTs to process data feeds, pastebins, tweets throught a message queue.


**Table of Contents**

1. [How to Install](#how-to-install)
2. [Goals](#goals)
3. [System](#system)
4. [IntelMQ Control Platform](#control-platform)
5. [Incident Handling Automation Project](#incident-handling-automation-project)


<a name="how-to-install"></a>
## How to Install

See [UserGuide](https://github.com/certtools/intelmq/blob/master/docs/UserGuide.md).


<a name="goals"></a>
## Goals

* Reduce the complexity of system administration
* Reduce the complexity of writing new bots for new data feeds
* Reduce the probability of events lost in all process (even system crash)
* Provide easy communication with other systems via API
* Use and improve the existing Data Harmonization Ontology
* Use the existing AbuseHelper Event-like syntax: event.add("domain", "example.com")
* Use JSON format for all messages
* Use messages tags: report, abuse-event, pastebin, tweet
* Integration of the existing tools (AbuseHelper, CIF, etc...)

<a name="system"></a>
## System


### Main Components
* RabbitMQ as message queue for pipeline
* Redis as memcache for bots


### System Architecture

(need update)
![System Architecture](http://i58.tinypic.com/n395bo.jpg)


### Code Architecture

(need update)
![Code Architecture](http://s28.postimg.org/uwzthgqrx/intelmq_arch.png)


### System Details

* Configuration: ... details ...
* How to dedup using Redis TTL: ... details ...
* Experts using Redis as a cache and TTL: ... details ...
* RabbitMQ Queues: ... details ...


<a name="control-platform"></a>
## IntelMQ Control Platform

![intelmq-control-platform](https://raw.githubusercontent.com/certtools/intelmq/master/docs/images/intelmq-control-platform.png?token=4184292__eyJzY29wZSI6IlJhd0Jsb2I6Y2VydHRvb2xzL2ludGVsbXEvbWFzdGVyL2RvY3MvaW1hZ2VzL2ludGVsbXEtY29udHJvbC1wbGF0Zm9ybS5wbmciLCJleHBpcmVzIjoxNDA4OTM5MzU2fQ%3D%3D--04d24c963f04d68cb22745e99f9389ab3d5fb147)

Check the [tool](https://github.com/certtools/intelmq-control-platform) and manage easily your IntelMQ system.

<a name="incident-handling-automation-project"></a>
## Incident Handling Automation Project

* **URL:** http://www.enisa.europa.eu/activities/cert/support/incident-handling-automation
* **Mailing-list:** ihap@lists.trusted-introducer.org

