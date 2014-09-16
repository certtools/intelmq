# IntelMQ

IntelMQ is a solution for CERTs to process data feeds, pastebins, tweets throught a message queue.


**Table of Contents**

1. [How to Install](#how-to-install)
2. [Goals](#goals)
3. [System](#system)
4. [IntelMQ Manager](#control-platform)
5. [Incident Handling Automation Project](#incident-handling-automation-project)
6. [Licence](#licence)


<a name="how-to-install"></a>
## How to Install

See [UserGuide](https://github.com/certtools/intelmq/blob/master/docs/UserGuide.md).


<a name="goals"></a>
## Goals

####  Version 1

* Reduce the complexity of system administration
* Reduce the complexity of writing new bots for new data feeds
* Reduce the probability of events lost in all process with persistence functionality (even system crash)
* Use and improve the existing Data Harmonization Ontology
* Use JSON format for all messages
* Integration of the existing tools (AbuseHelper, CIF, etc...)
* Provide easy way to store data into Log Collectors like ElasticSearch, Splunk, etc...
* Provide easy way to create your own black-lists

####  Version 2

* Provide easy communication with other systems via HTTP RESTFUL API
* Use messages tags: report, abuse-event, pastebin, tweet


<a name="system"></a>
## System


### Main Components
Redis is used as:
* message queue for pipeline
* memcache for bots


### System Architecture

(need update)
![System Architecture](http://i58.tinypic.com/n395bo.jpg)


### Code Architecture

(need update)
![Code Architecture](http://s28.postimg.org/uwzthgqrx/intelmq_arch.png)


<a name="control-platform"></a>
## IntelMQ Manager

Check the [tool](https://github.com/certtools/intelmq-manager) and manage easily IntelMQ system.


<a name="incident-handling-automation-project"></a>
## Incident Handling Automation Project

* **URL:** http://www.enisa.europa.eu/activities/cert/support/incident-handling-automation
* **Mailing-list:** ihap@lists.trusted-introducer.org

<a name="licence"></a>
## Licence

This software is licensed under GNU Affero General Public License version 3
