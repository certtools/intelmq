# System

## Goals

* reduce the complexity of system administration
* reduce the complexity of writing new bots for new data feeds
* reduce the probability of events lost in all process (even system down time)
* provide easy communication with other systems via API
* use and improve the existing Data Harmonization Ontology
* use the existing AbuseHelper Event-like syntax: event.add("domain", "example.com")
* use JSON format for all messages
* use messages tags: report, abuse-event, pastebin, tweet

## Main Components
* RabbitMQ as message queue for pipeline
* Redis as memcache for bots

## Architecture

![Architecture](https://bitbucket.org/ahshare/intelmq/downloads/poc_arch.jpg)

## System Details

* Configuration - <details>
* How to dedup using Redis TTL - <details>
* Experts using Redis as a cache and TTL - <details>
* RabbitMQ Queues - <details>

## How to install

Check doc/GUIDE.md file.


# Incident Handling Automation Project

* ** URL:** http://www.enisa.europa.eu/activities/cert/support/incident-handling-automation
* ** Mailing-list:** ihap@lists.trusted-introducer.org
* ** Data Harmonization Ontology:** https://bitbucket.org/clarifiednetworks/abusehelper/wiki/Data%20Harmonization%20Ontology

