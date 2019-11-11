# Idea list and architecture of IntelMQ 3.0

Author: Aaron Kaplan <kaplan@cert.at>

## Use-cases

## UX

### Devops/ Sysadmin perspective

#### Docker

**Task**: create a setup where each bot MAY run in a docker container

**Background**: It might make sense to  be able to run each bot in a docker container since it fits with a lot of new paradigms in orchestration.
With a proper template, each bot running in a docker container could send its logs to some central logger (for example splunk or similar) and 
the sysadmin/devops teams which are already using these systems for monitoring alerts can properly fit the IntelMQ logs and alerts to their regular daily routine.
Docker also allows the sysadmin/devops folks to centrally manage the system.

**Think about**: how do we integrate the pipeline graph?

**Category**: this feature should be OPTIONAL.

#### Tutorials and VMs / dockers

**Task**: create tutorials with VMs/docker images.

**Background**:
We are missing good tutorials ("playbooks") on how to run certain workflows via IntelMQ. Ideally, we would offer ready-made VMs/docker images where people who want to 
try out IntelMQ (and consequently adapt the setup to their own needs). This also helps teachers/presenters who want to demo IntelMQ.

Specifically we would like to have:
  * how to process shadowserver feeds
  * how to process shodan data
  * how to process n6 data

**Think about**: shadowserver already created some training material. Build on this.

**Category**: OPTIONAL component, but highly needed.


## Architecture



### Message queue

**Task**: Create a Kafka MQ backend: add Kafka as a replaceable MQ for IntelMQ 3.0

**Background**: IntelMQ 2.0 supports AMQP (RabbitMQ) next to redis as a message queue. Many organisations use Kafka internally. Support connecting to their other work flows.

**Think about**: 


**Category**: SHOULD




