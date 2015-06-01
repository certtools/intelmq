![IntelMQ](http://s28.postimg.org/r2av18a3x/Logo_Intel_MQ.png)

**IntelMQ** is a solution for CERTs for collecting and processing security 
feeds, pastebins, tweets using a message queue protocol. 
It's a community driven initiative called **IHAP** (Incident Handling 
Automation Project) which was conceptually designed 
by European CERTs during several InfoSec events. Its main goal is to 
give to incident responders an easy way to collect & process threat 
intelligence thus improving the incident handling processes of CERTs.

IntelMQ's design was influenced by 
[AbuseHelper](https://bitbucket.org/clarifiednetworks/abusehelper), 
however it was re-written from scratch and aims at:

* Reduce the complexity of system administration
* Reduce the complexity of writing new bots for new data feeds
* Reduce the probability of events lost in all process with persistence functionality (even system crash)
* Use and improve the existing Data Harmonization Ontology
* Use JSON format for all messages
* Integration of the existing tools (AbuseHelper, CIF)
* Provide easy way to store data into Log Collectors like ElasticSearch, Splunk
* Provide easy way to create your own black-lists
* Provide easy communication with other systems via HTTP RESTFUL API

It follows the following basic meta-guidelines:

* Don't break simplicity - KISS
* Keep it open source - forever
* Strive for perfection while keeping a deadline
 * Reduce complexity/avoid feature bloat
 * Embrace unit testing
 * Code readability: test with unexperienced programmers
* Communicate clearly

Visit [Wiki page](https://github.com/certtools/intelmq/wiki/).
