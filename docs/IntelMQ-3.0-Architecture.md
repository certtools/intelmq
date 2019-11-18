# Idea list and architecture of IntelMQ 3.0

Author: Aaron Kaplan <kaplan@cert.at>

## Use-cases

XXX fill in a complete list of use cases XXX

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

_Think about_: 


_Category_: SHOULD




