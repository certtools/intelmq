![IntelMQ](http://s28.postimg.org/r2av18a3x/Logo_Intel_MQ.png)

**IntelMQ** is a solution for CERTs for collecting and processing security feeds, pastebins, tweets using a message queue protocol. It’s a community driven initiative called **IHAP** (Incident Handling Automation Project) which was conceptually designed by European CERTs during several InfoSec events. Its main goal is to give to incident responders an easy way to collect & process threat intelligence thus improving the incident handling processes of CERTs.

IntelMQ's design was influenced by [AbuseHelper](https://bitbucket.org/clarifiednetworks/abusehelper), however it was re-written from scratch and aims at:
* Reduce the complexity of system administration
* Reduce the complexity of writing new bots for new data feeds
* Reduce the probability of events lost in all process with persistence functionality (even system crash)
* Use and improve the existing Data Harmonization Ontology
* Use JSON format for all messages
* Integration of the existing tools (AbuseHelper, CIF)
* Provide easy way to store data into Log Collectors like ElasticSearch, Splunk
* Provide easy way to create your own black-lists
* Provide easy communication with other systems via HTTP RESTFUL API


## Table of Contents

1. [How to Install](#how-to-install)
2. [IntelMQ Manager](#control-platform)
3. [Incident Handling Automation Project](#incident-handling-automation-project)
4. [Data Harmonization](#data-harmonization)
5. [Licence](#licence)


<a name="how-to-install"></a>
## How to Install

See [UserGuide](https://github.com/certtools/intelmq/blob/master/docs/UserGuide.md).


<a name="control-platform"></a>
## IntelMQ Manager

Check the [tool](https://github.com/certtools/intelmq-manager) and manage easily IntelMQ system.


<a name="incident-handling-automation-project"></a>
## Incident Handling Automation Project

* **URL:** http://www.enisa.europa.eu/activities/cert/support/incident-handling-automation
* **Mailing-list:** ihap@lists.trusted-introducer.org


<a name="data-harmonization"></a>
## Data Harmonization

IntelMQ use the Data Harmonization. Check the following [document](https://github.com/certtools/intelmq/blob/master/docs/DataHarmonization.md).

<a name="licence"></a>
## Licence

This software is licensed under GNU Affero General Public License version 3
