<!-- comment
   SPDX-FileCopyrightText: 2019 aaronkaplan <aaron@lo-res.org>
   SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Idea list and architecture of IntelMQ 3.0

Authors: Aaron Kaplan <kaplan@cert.at>, Sebastian Wagner <wagner@cert.at>

## Use-cases

XXX fill in a complete list of use cases XXX

### CERTs

No direct access to networks in constituency.

#### Data collection

#### Distribution of information

#### National CERT

Work is based heavily on Geolocation

#### Sector CERT

Work is based on known constituents, sector information, lists of IP address ranges and domains, company & organisation names.

### SOCs and NOCs

Goal is the protection of internal known networks only. Direct access to the networks.

Involves collecting information from internal infrastructure, matching IoCs to internal infrastructure, using IoCs for active protection.

### Data science and research

## Users

XXX fill in a complete list of use cases XXX

## RESTful API

For automation purposes, we will need a typical RESTful API to manage, control, monitor the IntelMQ "botnet" and read and set configs.
See [#1424](https://github.com/certtools/intelmq/issues/1424)

## UX




### Devops/ Sysadmin perspective

#### Docker

_Task_: create a setup where each bot MAY run in a docker container

_Background_: It might make sense to  be able to run each bot in a docker container since it fits with a lot of new paradigms in orchestration.
With a proper template, each bot running in a docker container could send its logs to some central logger (for example splunk or similar) and 
the sysadmin/devops teams which are already using these systems for monitoring alerts can properly fit the IntelMQ logs and alerts to their regular daily routine.
Docker also allows the sysadmin/devops folks to centrally manage the system.

_Think about_: how do we integrate the pipeline graph?

_Category_: this feature should be OPTIONAL.

#### Tutorials and VMs / dockers

_Task_: create tutorials with VMs/docker images.

_Background_:
We are missing good tutorials ("playbooks") on how to run certain workflows via IntelMQ. Ideally, we would offer ready-made VMs/docker images where people who want to 
try out IntelMQ (and consequently adapt the setup to their own needs). This also helps teachers/presenters who want to demo IntelMQ.

Specifically we would like to have:
  * how to process shadowserver feeds
  * how to process shodan data
  * how to process n6 data

_Think about_: shadowserver already created some training material. Build on this.

_Category_: OPTIONAL component, but highly needed.


## Architecture



### Message queue

_Task_: Create a Kafka MQ backend: add Kafka as a replaceable MQ for IntelMQ 3.0

_Background_: IntelMQ 2.0 supports AMQP (RabbitMQ) next to redis as a message queue. Many organisations use Kafka internally. Support connecting to their other work flows.

_Think about_: Using [Apache Pulsar](https://pulsar.apache.org/)


_Category_: SHOULD


## Notification settings

_Task_: Keep notification settings per event: Where to (destination mail/host address), how (protocol, authentication (SSL client certificate), etc), how often/time information (intervals etc.)

_Background_: CERTs (and potentially other groups of users) need to specify where the events should be sent to, how often etc. Currently only destination email addresses can be saved (`source.abuse_contact`), which is not enough for most use-cases. There exist some custom solutions (e.g. `notify` boolean at cert.at (to be changed), `extra.processing` dictionary at BSI), but no least common denominator.

See also https://github.com/certtools/intelmq/issues/758

_Category_: this feature should be OPTIONAL but is NEEDED by several users.


## Configuration parameter handling in Bots and a bot's unified documentation

_Task_: Handle bots' configuration parameters by the core, providing type sanitation, checks, default values and documentation.

_Background_: Currently every bot needs to handle these issues itself, but many of these checks could be done centrally in a generic way. At upgrades, new configuration might get introduced and the bots need to provide defaults values although they are available in BOTS. Error handling on parameters must be done for every bot on itself. Documentation is not available to the Bots, not available in BOTS and the Manager. There are 3 places for parameters where the available information is spread: BOTS, `Bots.md` and the bots' code.


## Automatic Monitoring & Management: Handling full load situations

_Task_: Create a solution to prevent system over-loading (only for Redis).

_Background_: If too much data is ingested, collected or enriched, the system can easily run out of memory. This quickly causes major operation troubles and data loss, needing manual intervention.

See also: https://github.com/certtools/intelmq/issues/709


## Making intelmq plug-able and getting rid of BOTS

_Task_: Allow installation of IntelMQ bots, meaning the deprecation of the centralized BOTS file and a generated documentation.

_Background_: Adapting IntelMQ to specific needs also means the development of specific bots which might not part of the public repository. Adding them to an existing IntelMQ installation is currently only possible by cloning the repository and adding the code there, not by just providing/installing the required code (because of BOTS and central documentation).

See also https://github.com/certtools/intelmq/issues/972


## Exposing a plug-in or hooking API

_Task_: Provide an hooking API for the core classes.

_Background_: Adapting IntelMQ to specific can require adaptions in the Core classes' code. Instead of making the changes/extensions in the core itself, we can provide a hook system allowing to call (or replace?) functions at specific steps. For example custom monitoring.


## Grouping of events

_Task_: Provide possibilities to assign an event to a group of events.

_Background_: Several IoCs part of one MISP Event. Grouping of similar events to one group for outputs (e.g. one CSV file per Network).

See also: https://github.com/certtools/intelmq/issues/751

## Data Format: Multiple values

_Task_: Allow multiple values for (some) fields in the data format.

_Background_: In some cases one value per field is not enough, for example for Domain -> IP address lookups. Other formats like IDEA and n6 support this.

See also: https://github.com/certtools/intelmq/issues/543 https://github.com/certtools/intelmq/issues/373
