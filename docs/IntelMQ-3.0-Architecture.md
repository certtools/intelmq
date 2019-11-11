# Idea list and architecture of IntelMQ 3.0

Author: Aaron Kaplan <kaplan@cert.at>

## Use-cases

## UX

### Devops/ Sysadmin perspective

#### Docker
It might make sense to  be able to run each bot in a docker container since it fits with a lot of new paradigms in orchestration.
With a proper template, each bot running in a docker container could send its logs to some central logger (for example splunk or similar) and 
the sysadmin/devops teams which are already using these systems for monitoring alerts can properly fit the IntelMQ logs and alerts to their regular daily routine.

This feature should be OPTIONAL.


## Architecture



### Message queue

IntelMQ 2.0 supports AMQP (RabbitMQ) next to redis as a message queue. 

* Add Kafka as a replaceable MQ for IntelMQ 3.0


