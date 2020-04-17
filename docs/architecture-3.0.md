Thoughts INTELMQ 3.0
======================



# Motivation

IntelMQ was created as a viable, easier alternative to Abusehelper roughly 2014/2013. 
At this time, the fathers of IntelMQ (Tomas Lima, then CERT.pt, Aaron Kaplan, CERT.at) focused on easy ("KISS principle") to understand code and open source.

In the mean time, IntelMQ became a de-facto standard for automatic incident handling for many European CERTs.

However, the success also resulted in IntelMQ being used in contexts which were not anticipated. Also, running a production instance of IntelMQ gave us new requirements - mainly from the side of running it within a corporation or larger team where operations of systems is separated from the development side.

In short, IntelMQ needs to support more standard processes which can be found in regular IT operations: monitoring & alerting, central logging & control, scalability sizing , containerisation etc.

The following proposal shall address these issues and is meant as a basis for discussion with the IntelMQ users.

If something is missing from the list, if something is not important at all or very important, etc. please let us know.

We are happy to receive your feedback.

Aaron Kaplan  - IntelMQ 3.0 Architecture.
kaplan@cert.at



# Architecture


![architecture of a bot in IntelMQ 3.0](images/intelmq3.0-architecture.png)


## Microservice architecture

This should be compatible with the standard nic.at micro service architecture.
It however needs to be flexible enough to allow other teams to integrate it very easily into their architecture.
Therefore, the definitions of the architecture needs to be cross checked with the major players in this field (cert.pl, cz-nic, Iain, IHAP group, ...)

The high level goals of using a micro service architecture for IntelMQ 3.0 are:

  * we want to be highly maintainable on an individual (bot- or functionality) level
  * we want to be highly testable in a _standardized_ way. Calling a test function for a bot shall be identical. Tests consist of a) unit tests of the microservice but also b) of integration tests of the micro service with its environment. The self-test shall be run on the current config of the bot/container.
  * a micrsoservice allows for self-inspection: within the context of IntelMQ's bots this means that a bot knows which input it needs to be able to work properly (i.e. which DHO fields are filled out) and which fields it produces. This allows for integration tests.
  * bots must be independently deployable and a deployment must be *self-contained*.  No fiddling should be needed. It should be as easy as docker-compose ... if a microservice needs to install or fetch external resources (example a DB) before it is ready, it shall do that in the init() function and only then report that it is finished.
  * each micro service MUST focus on one and only one task and excel at doing it
  * each micro service MUST be maintained by a small team. One developer is not enough. There shall be a clear point of contact relationship for each micro service, hence... Think metadata on a bot/container. 
  * a micro service is registered at a registry of IntelMQ 3.0 micro services (which must contain the latest version number, contact info for the developer team, etc)
  * a microservice MUST support service discovery. It shall register itself at some orchestrator - compare with registry.
  * a microservice MUST support monitoring tools (check_mk, etc) and report its status to a monitoring tool
  * a microservice MAY support Identity mgmt tools via OpenID Connect on its' API
  * a microservice MUST be very easily integratable in other frameworks and work-flows. Think: IntelMQ 3.0 micro service components may run (as micro services) within a bigger data processing tool.
  

All of these requirements point towards a container architecture with standardised RESTful API endpoints.
The RESETful API SHOULD be implemented on the basis of the OpenAPI specs.
(Note: look at JSON API specs)



### Framework: let's go containers!

Docker based. nic.at is moving gradually to docker. So is the rest of the world.
Docker allows new users to very quickly try out a setup. It lends itself to tutorials and experiments, it helps with orchestration. 
However, we do not want to have a complete buy-in to any particular container tech stack. IntelMQ 3.0 should be flexible enough to be embedded in an alternative container tech stack. However, docker will remain the #1 option since it is the most commonly used one.

The container stack allows us to have every single bot equipped by a default (but changeable) set of dev-ops/ops features for the use-case of running the bot in a controlled sysadmin/ops environment.

If we look at the list of high level requirements from above, we can become more specific.

Our docker template for a bot shall provide a RESTful API

### RESTful API requirements

  
  * It must be well documented (OpenAPI specs)
  * an example hello world with the API exists on GitHub

  * The micoservice API MUST support 
    * basics:
      * starting/stopping/reload/restarting/pausing a bot 
      * inspecting and setting it's runtime parameters of the bot
      * getting version infos and meta-information on the bot + container
        * especially a list of required input fields and produced output fields (-> introspection)

    * tests:
      * triggering a config test (bot intelmqctl configtest)  --> are the runtime params OK, internal python bot config test. No connections are made
           https://<url-of-my-docker-container>/api/v1/self-test/config-test
      * triggering a connectivity test (i.e. can it send/receive data? connections to DBs)
          Are all required connections (redis, DB, input / output of network ) ready?
        https://<url-of-my-docker-container>/api/v1/self-test/connection-test

      * triggering a self-test (unit-test)
          python unit tests

      * triggering a system-test (i.e. does it get the data that it needs? can it do its task and can it send out the data that it sends out?)
          actually check if it can/could get all the input fields it needs. This is a global test. The MS can send the field names it needs and the field names it produces.


    * connectivity:
      * API endpoints for configuring the pipeline of the bot as well as the MQ stack


    * operations specifics:
      * an API endpoint to dump the current state of the bot to disk so that this container may be paused and migrated to a different system.  --> TBD
      * monitoring information (health check, alerts, data rates of the flows, error counters, etc)
      * registering callbacks (or configuring the necessary infos) for a monitoring solution such as check_mk, nagios
(introspection)
      * report (in the documentation) on the rough requirements on RAM, disk space, CPU load etc. - think base-line 
      * endpoints for configuring syslog flows (where should the bot send it to)
      * Data freshness check is built-in (to be defined below)

    * IAM / Authentication & Authorization
      * If authentication is needed, a Bot SHOULD support OpenID connect on it's REST interface 
      * MAYBE also  setting encryption settings on the M2M interface (the MQ) ?

    * developer support
     XXX ideas? XXX
      * how can we expose / should we expose the debug method of the bot to the container?



Using the docker template bot, a bot needs to connect to the provided software layers which interface the functionalities described above

### An IntelMQ 3.0 docker-bot now consists of:

  1. the IntelMQ bot per se (and corresponding libraries)
  2. the means to connect the container and bot to other containers/bots
  * the means to instrument the data flowing in and -out (--> monitoring)
  * the means to replace the connection / MQ stack (on a per bot / container level).
    
  * a standard test 
  * self-reporting to a central instance (orchestrator / registry)
  * standardised logging
  * standardised self-test
  * integration into check_mk or other monitoring solution
  * standardised REST-api for the bot (start, stop, status)
  * status queries to the bot (health, number of events/sec, etc)
  * test "would this botnet setup work?" / test if a bot in this pipeline could function (-- > introspection of what data is needed for the bot and what data it provides)
  * docker scale it horizontally --> data processing bottlenecks? --> horizontal scaling should be a click of a button
  * standardised way to self-update any external dependencies (maxmind, etc) & report alert if something goes wrong
  * standardised alerting mechanism (--> check_mk for nic.at)


### Data freshness

  * check if the needed databases (for example maxmind) is the latest version and download it if needed
  * self-updates per se are *not* supported. Patching must be done from the outside.


# IntelMQ 3.0 specifics

These are independent of the container stack


## MQ: Replaceable MQ & support for Kafka

## Transformers

new class of bots: transform one data format (e.g. DHO) to another one (e.g. IDEA) or n6 <-> DHO


## Outputs: Really good out of the box support for ELK and Splunk 

out of the box support


## Internal code: more modern python version with typing. Typing and type hints support in all of the code base

* mostly done. The core already supports the most important functions.

## n6 interoperability

## domain based workflow

## portal-integration?

  * TBD

## DHO 2.0

  * we need to support structs / lists of fields (or structs). One step towards IDEA and/or n6. This task is highly dependant and basically the core of the n6<-> intelmq interoperability.
  * machine readable specs of the DHO 2.0
  * mapping of DHS 2.0 to other formats

## XXX aaron review #arch tag on GitHub


## RESTful API requirements

We don't care which API framework you want to use (hug, fast api, flask, ...)
What we do care about is the RESTful API interface 
We created a template API spec <insert link>


TODOs Aaron
=============
* add pics / better explanations
* put to GitHub
* clarify with ops/Alex
* post to IHAP and intelmq-users/+dev
* call Bernd
* cross check with Jaroslaw
* template API spec

TODOs sebix
===========
* cross check with CEF proposal



