# Architecture of INTELMQ 3.0

Author: Aaron Kaplan <kaplan@cert.at>

Version: 0.8


# Scope

The following architecture document addresses 

  * an architecture discussion for IntelMQ 3.x. This version should be seen as a re-alignment on IntelMQ's core 
  principles which got lost over the last years due to feature creep
  * making IntelMQ 3.x interoperable with CERT.pl's n6 system

## Implementation evaluation
The mayor changes listed in this document should be evaluated based on use-cases and technical feasibility before the final implementation and integration into IntelMQ. The exact details of this process will be defined later."

# Non-Scope

This document will not list the individual, detailed steps which need to be taken to achieve these goals. 
This is a high-level overview document. The detailed, individual steps will be specified as individual 
issues on github and assigned to the milestone `3.0`: https://github.com/certtools/intelmq/milestone/16


# Motivation & Introduction

IntelMQ was created as a viable, easier alternative to AbuseHelper roughly 2014/2013. 
At this time, the fathers of IntelMQ (Tomas Lima, back then CERT.pt, Aaron Kaplan, CERT.at) focused on 
easy to understand code ("KISS principle") and open source.

In the mean time, IntelMQ became a de-facto standard for automatic incident handling for many European CERTs.
This success also resulted in more code, feature creep, some complex and harder to understand code and it also 
resulted in IntelMQ being used in contexts which were not anticipated. In addition, running a production instance 
of IntelMQ gave us new requirements - mainly from the side of running it within a corporation or larger team where 
the operations of systems is a separated organisational unit from the development side.
Finally, as more teams started to use IntelMQ, weaknesses with respect to user-friendliness became visible. 
This became especially apparent at user-trainings (at TF-CSIRTs, etc.), which clearly show that many of 
IntelMQ's 2.x features are totally non-intuitive. 
Often, from a user's perspective, it was not clear that a feature was present unless you read the source code or 
followed all of the development stream. This is mainly due to the fact 
that IntelMQ 2.x and large parts of 1.x were developed by one single core developer and were not discussed enough 
in a wider user group.

The way out of this dilemma (and out of feature creep) is to focus on 

  - a) simplicity (i.e. **reduce complexity**, **follow a unix philosophy**) and 
  - b) standardised procedures which are now (as of 2020) common in the field (with plenty of examples of data-flow 
  oriented architectures to copy from). 

In short, IntelMQ needs to **support more standard processes** which can be found in regular IT operations: 
microservices, monitoring & alerting, central logging & control, scalability sizing, containerisation etc. 
It also needs to behave more as expected / **"turn-key" out of the box**. 
It needs to orient itself at other (larger) standard tools (such as Elastic Search), which show how it's done. 
This can be achieved by integrating it better with the existing most commonly used operations tools that teams 
use (e.g. centralized monitoring and alerting, etc). Cross connecting IntelMQ instances for automatic data 
exchanges as well as the planned IntelMQ-to-n6 interoperability adds new requirements. 

The main point however is: **IntelMQ needs to be more user-friendly** and **fulfill the user's default expectations**.

Hence the following document shall lay out the architectural foundations for an IntelMQ 3.0 release.

This document shall also propose a governance mechanism for the community-driven IntelMQ project.

The following proposal shall address these issues and is meant as a basis for discussion with the IntelMQ users.
If something is missing from the list, if something is not important at all or very important, etc. please let us know.
We are happy to receive your feedback.

**Why we need this document**

The main benefit of this document shall be that:
  1. we have a roadmap for IntelMQ 3.0 and beyond. This roadmap shall ensure that IntelMQ stays relevant for the future.
  2. that we start some formal community-formation around IntelMQ which will give the project a much longer life compared to
   when it is "only" maintained at CERT.at
  3. we have a basis for discussion on how the project shall move forward for the whole community of IntelMQ users 
  and developers.

Aaron Kaplan  - IntelMQ 3.0 Architecture.
<kaplan@cert.at>, <aaron@lo-res.org>



# Overall architecture of IntelMQ 3.0 & the soul of IntelMQ 

The overall architecture of IntelMQ 3.0 will remain rather similar to version 2.x (i.e. we will still have a 
data-flow oriented architecture, "bots" and "botnets"). But we plan to have a few important changes, which will 
emphasize the "soul" of IntelMQ.

## The soul of IntelMQ

**Note**: the following section is a recap of what the original inventors had in mind and why IntelMQ exists.

IntelMQ was invented and is good for a **specific purpose**. It is:

 * An **[ETL](https://en.wikipedia.org/wiki/Extract,_transform,_load) (Extract Transform Load) tool** for
 * **[IoCs](https://en.wikipedia.org/wiki/Indicator_of_compromise)** and **IT security relevant events** (i.e. IT security log lines which contain a timestamp, IPs or domain names and context information)
 * a set of libraries and tools which are composable and roughly follow the **[Unix Philosophy](https://en.wikipedia.org/wiki/Unix_philosophy)**
 
IntelMQ was **not** meant to be a tool for:

   * general Threat Intelligence correlation and - pivoting (c.f. [MISP](https://www.misp-project.org))
   * a general solution for processing arbitrary streams of logs (see Splunk, ELK, etc.) - IntelMQ focuses on a typical log lines for IT security purposes only (that is - timestamp, IPs or domain names, context information)

There are many data-flow oriented architectures (by now) which do similar things to IntelMQ. However, 
to the best of our knowledge none (except for AbuseHelper) focuses on IoCs and CSIRTs. So this separates IntelMQ 
from more generic data-flow oriented architectures such as Airflow, Kafka, Apache Pulsar etc.
(now, in 2020, it will be important to **connect** to these other systems).

Let us dig deeper into this topic the foundations of IntelMQ, but first, we should review aspects of the Unix philosophy:

>In their preface to the 1984 book, The UNIX Programming Environment, Brian Kernighan and Rob Pike, both from Bell Labs, give a brief description of the Unix design and the Unix philosophy:

>> *"Even though the UNIX system introduces a number of innovative programs and techniques, no single program or idea makes it work well. Instead, what makes it effective is the approach to programming, a philosophy of using the computer. Although that philosophy can't be written down in a single sentence, at its heart is the idea that the power of a system comes more from the relationships among programs than from the programs themselves. Many UNIX programs do quite trivial things in isolation, but, combined with other programs, become general and useful tools."* (Source: [Wikipedia](https://en.wikipedia.org/wiki/Unix_philosophy#The_UNIX_Programming_Environment))


Next, let's look at the specific purposes and use-cases listed above:

  * **ETL**: as an ETL user, I want something which can 
    - go over large amounts of data possibly in parallel
    - do the complex parsing and validation work for me
    - filter out rows which are unusable (but keep them somewhere for re-runs)
    - ideally be used as both a (python) library which does that and as a command line tool
    - map input fields to IDF ("Internal Data Format", see the IDF section)
    - allow for plugging in arbitrary transformations (-> experts and output programs in our case)
    - load the data into some other system (-> output programs: postgresql, Elastic Search, Splunk, etc.)
    - be automated, once I am sure I can run through the data safely every time
  * **IoCs**: IntelMQ MUST support the most common IoC / it security logs which CERTs encounter: shadowserver, team cymru, etc. etc.
    One format that IntelMQ does not support yet, is STIX 2.x (input). It is widely used by many tools. We should support it.
    In general, with IoCs on the input side, IntelMQ 1.x and 2.x are already very solid. There is a strong foundation on which to build. Very little needs to be changed here for IntelMQ 3.0
  * **composable tools**: here, IntelMQ 3.0 needs to do better. Let's expand this in the next paragraphs.


If we take the core ideas of IntelMQ to heart, and carefully read the **principles of the Unix Philosophy** we arrive at the following mantras:

  * **keep it simple** (KISS): 
    - --> don't create a program which can do everything! Split it up. Each component shall be **independent** and [Do one thing and do it well](https://en.wikipedia.org/wiki/Unix_philosophy#Do_One_Thing_and_Do_It_Well). Don't add diverging features into one component / program / config file.  If it tries to do everything in one single config file, you missed a point.
      - This also implies: if you need to modify the behaviour of the specific component, configure it independently
      - if the program needs to do variations of its job, use command line parameters (config options)
    - --> Fewer lines of code are better (if it still gets the job done)
    - --> document each component (bot) and show how it can be used with examples. Take a look at the structure of man pages.
    - --> strengthen the review process of submissions: is that really the most easily understandable code for the task?
    - no task / program is too trivial: take a look at the unix <code>cat</code> program. It's super versatile, yet simple. Think of adding many of these simple bots/programs/components.
  * **interoperability and networking of programs**: 
    - the easiest and first interoperability mechanism is: **"librarize" everything first!**:
      - If you have a new IntelMQ bot or expert, make a python library out of it, **which may/should/could be used independently** (note: this also solves #[972](https://github.com/certtools/intelmq/issues/972)).
      - document this library in a standard fashion (i.e. readthedocs)
      - give example code in the documentation (e.g. link back to source code in the IntelMQ framework / a bot, which uses this library)
      - make this library available and installable via standard methods (e.g. pypi, pip install, conda)
      - name this library ``pyIntelmq-*foo*`` 
    - next after releasing functionality of IntelMQ bots as a library, have a bot which uses this library. This bot now needs to get the data from somewhere and send it somewhere:  
    - allow for arbitrary but standardized interconnections (in the unix philosophy: pipes)
    - --> in our case this calls for an abstracted message queue (pipes are linear<sup>[1](#fn_1)</sup>)
    - --> allow for easy interconnection with other IntelMQ-like tools or other tools 
      * the easiest such solution is to allow for <code>stdin, stdout</code> connections between bots
      * the next easiest solution is named pipes
      * after this, go for message queues (redis, AMQP, Kafka, etc.)
  * **documentation**: Unix has very well written man pages. These again focus on one program (or even on parts of a program) and one topic. (IntelMQ is missing this individual man pages approach per bot so far).
  * **usability**: focus on usability (from the ETL coder's perspective)
    - --> this nowadays means that it shall be easy to understand, extend, connect, embed IntelMQ **or individual bots without the whole IntelMQ framework** into your workflows.


If you think of some future architecture decisions or features: think about these aspects.


## Consequences of these principles for IntelMQ 3.0

### Terminology

Since IntelMQ's new networking requirements also ask for one-time runs with <code>stdin, stdout</code> connections (or arbitrary connections), IntelMQ "bots" become more like "programs" (as in unix programs or one time or periodically (cron) running programs) or more like "daemons" (as in background task which listens on network connections or message queues, names pipes, ... and answer a request). Expert bots fall under that latter category.

We therefore propose to rename an IntelMQ "bot" to "IntelMQ worker" or "IntelMQ component". From now on through the rest of the document, will use this new terminology. Note that "bot" is the old term.

Similarly, we shall rename an IntelMQ "botnet" to "workflow". This is the more standardized nomenclature.

We shall rename the "DHO" (data harmonization ontology) to "internal data format" (IDF). 

The names "collector", "parser", "expert" and "output (program)"  shall remain.


### Relationship to microservices

Microservices provide a very nice web-based wrapping mechanism for IntelMQ programs and daemons.
Imagine an "expert" program which takes as input an IP address and returns the current ASN of this IP ([asn_lookup](https://github.com/certtools/intelmq/tree/develop/intelmq/bots/experts/asn_lookup)). With the library approach, it is trivial to write a microservices around this.

In addition, microservices allow IntelMQ to scale horizontally quite easily (--> see the chapter on scaling)

Since the IntelMQ user-survey clearly revealed that docker/microservice approaches are OK, but should not be 
enforced on the IntelMQ user base, we therefore propose to go the "librarize" approach first, and as a second 
step to wrap all IntelMQ daemons / programs into microservices. These are a CERT.at specific requirement for 
CERT.at's parent company. Hence these microservices shall reside in 
[CERT.at's github repository](http://github.com/certat/) or 
[nic.at's github repository](https://github.com/nic-at) only. 
These microservices **MUST** follow the nic.at microservice HOWTO.

One benefit of using the microservice / docker approach will be that each IntelMQ program/daemon wrapped in a 
docker container  shall have an accompanying ``statusd`` daemon, which shall collect status information from the 
bot (i.e. flow rate of requests / sec, error rate, etc.) and report it via a standardized reporting / monitoring 
tool (such as prometheus). IntelMQ users of the microservice approach will profit from this monitoring approach.
In fact, this was the most important finding while doing interviews with multiple IntelMQ users. Currently, 
``intelmqctl`` is used as a sort of control channel. however, it does not scale and it's not fast enough. It 
would make more sense to have a type of "``intelmq-statusd``" (daemon) process which does not need to be invoked 
for every query (as is the case with the command line intelmqctl script). The ``intelmq-statusd`` would povide a 
short and lean RESTful API to the outside world, which will manage signaling of the bot / botnet and be able to 
query a bot's or botnets' status. See the architecture diagram below.
 

![architecture of an IntelMQ 3.0 program](images/intelmq3.0-architecture.png)

### Relationship to an "IntelMQ API"

Issue #[1424](https://github.com/certtools/intelmq/issues/1424) proposes an API for IntelMQ. This idea has been 
around for some time already before and it definitely would be an interesting addition.
We propose to first create a simple HTTP(s) microservice API for each individual microservice (as described above).
Next, in a minor version after 3.0 we shall consider creating an API which covers the whole work flow.
This extension will be rather easy when the individual microservice API is working.

The individual microservice API shall cover all the basic commands which ``intelmqctl`` offers for a single bot.

For IntelMQ 3.0 we should first compare against the new ``intelmq-manager`` (the proposal and development of Intevation) first
before the API gets (re-) invented.


### Documentation
 
  * Each IntelMQ library shall be documented (as described above) independently in its own read-the-docs site and/or man page.
  * An intelMQ program / daemon shall have its own documentation (linking to the library which it uses)
  * Tutorials: plenty of tutorials and sample workflows on how to get something done with IntelMQ 3.0 are needed.
  * Each IntelMQ library and program shall have a named (email address is enough) maintainer. It MUST be part of 
  the documentation.
  * Create a documentation template for new IntelMQ programs.
  * Licenses: ensure correct licensing information exists for every component (c.f. tools by the FSF & co.)


### Networking

IntelMQ 3.0 shall support the following input / output channels / networks:

  * stdin, stdout (especially for one-time runs)
  * redis queues (to be precise: [redis lists](https://redis.io/topics/data-types) being used as FIFOs already)
  * [redis streams](https://redis.io/topics/streams-intro)
  * Apache Kafka
  * RabbitMQ / AMQP
  * Apache Pulsar

### Interoperability with CERT.pl's n6 system

IntelMQ 3.0 shall add a thin wrapper layer to wrap n6 programs. The goal is to be able to embed n6 "bots" 
(programs) into an IntelMQ workflow. The other direction (embedding IntelMQ into n6) was already achieved by 
CERT.pl. The wrapper mainly consists of a IDF to n6's internal format translation / mapping layer. See also the 
IDF section. Since the new IDF shall support multiple values, mapping to n6 should be rather easy.


### Internal data format (IDF)

Note: formerly called ["DHO"](https://github.com/certtools/intelmq/blob/master/docs/Data-Harmonization.md)

**Note: This is probably the change with the most impact. It will need special attention.**

#### Reasons for the changes

The previous philosophy of the (old) DHO format was:

  - keep a flat log-line entry structure (flat, but just in JSON). 
  - allow for one sub level, separated by ".". For example a field name would be "source.ip"
  - arbitrary (but not standardized) deeply nested data was possible in the ``extra`` JSON dict sub-field. For example: ``"extra": { "foo": "bar", "some-metric": 1.0 }`` (which 
got mapped to "extra.foo" internally)



It turned out (and this was also the feedback from the survey) that this structure was not sufficient for 

  - interoperability with other tools such as CERT.pl's n6 or [Warden](https://www.cesnet.cz/sluzby/warden/)
  - the subject at hand: i.e. most of the time, it's sufficient to talk about a single IP address, but sometimes one incident requires the sender to specify multiple IPs or domain names or other fields. 

#### General requirements

The new IDF shall support 
  - (sorted) lists of IPs, domains, taxonomy categories, etc. 
  By convention the most relevant item in such a list MUST be the first item in the sorted list.
  - a ``meta`` field (which describe the IDF version. See below)
  - packing multiple events (log lines) into one "packet" (i.e. one ``meta:`` field, ``data`` 
  becomes an array of events). See issue #[1541](https://github.com/certtools/intelmq/issues/1541).


The IDF MUST be represented by a JSON schema which MUST reside in the intelmq repository.

The IDF ``meta`` field MUST exist and is a header, which in turn MUST contain a 
  - data format name (``IntelMQ-IDF``)
  - a version number
  - a link to the format description (URL)
  - a source (emitter) tag (a unique string) - think UUID  

The IDF SHALL be user-expandable (see #[1315](https://github.com/certtools/intelmq/issues/1315)). This fits nicely into a sub-section within the JSON API ``data`` section. For example: ``data.custom.*``.


#### Format specifics

The IDF SHOULD follow the [JSON API specifications](https://jsonapi.org/format/).

**Within** the JSON API's ``data`` block, the field names SHALL conform to the [ECS](https://www.elastic.co/guide/en/ecs/current/ecs-field-reference.html) where possible.
Example: the field ``source.asn`` will be renamed to ECS's (source.)``as.number``.
The [ECS version number](https://www.elastic.co/guide/en/ecs/current/ecs-reference.html#_maturity) (``ecs.version``) shall be noted in the JSON API's ``meta`` field.

If a field does not exist in the ECS, please follow ECS's official guidelines on 
how to map it: 
https://www.elastic.co/guide/en/ecs/current/ecs-reference.html#_my_events_dont_map_with_ecs (i.e. just write the field name, ECS is permissive). Please also see the [ECS migration guide](https://www.elastic.co/guide/en/ecs/current/ecs-converting.html)


The reasoning behind adopting ECS for IntelMQ 3.0 is 

 - originally IntelMQ chose something inbetween Elastic Searches' format ("." separated fields) and Abusehelper's format. Now, in 2020, it's pretty clear which product gained traction: Elastic Search.
 - being compatible with ECS is a big win for IntelMQ and ELK integration.

A mapping table between the (old) DHO and the new IDF format shall be written.
This mapping table will allow for converter IntelMQ-programs between the old format and the new IDF.

#### Example

```json
{ "meta": 
  { "version": "3.1", 
    "format-name": "intelmq", 
    "url": "https://github.com/certtools/intelmq/docs/IDF-format.3.1.md",
    "created-at": "2020/5/1 12:00:00+0", 
    "producer": "cert.at" }, 
  "data": [ { dict...}, {dict ...},... ] 
}
```


  

### Logging

This is already quite mature in IntelMQ 1.x and 2.x. No changes needed.

### Run-modes and parallelization

An IntelMQ program shall support at least two run-modes:

  - one-time run: 
    - here all data on the input side (stdin, network, message queue) shall be consumed or, 
    - *optionally*, at most *n* elements shall be consumed ( to be specified on the cmd line)
    - such an intelMQ programm shall be call-able from the command line. Example: 
    ```bash
    $ intelmq-shadowserver-collector --config /etc/intelmq/config.d/ss.conf --stop-after 1000 < input.txt
    ``` 
  - daemon mode (continuous):
    - this is pretty much the de-facto run mode of IntelMQ 2.x and 1.x: the daemon listens on some network connection or message queue (or named pipe) for input and processes it, one at a time.
    - a **new feature here** is the support for automatic parallelization: by specifying the number of copies of the daemon, a user can create a "fan-out" parallelization on some given input queue. Example:
    ```bash
    $ intelmq-shadowserver-collector --daemon --config /etc/intelmq/config.d/ss.conf --processes 20
    ``` 
    This shall start 20 processes in parallel which take turns in processing the input queue.

### Scalability 

If you combine the docker/containerization aspects and the ``--processes X`` option, you end up with a highly scalable solution.
(given that experts still refrain from doing online (network) lookups for every event). It is still highly advisable that experts shall fetch a local copy of some reference data set and do the lookup on this refernce data set locally.


### Configuration files

First of all, we need to get rid of the BOTS file. See issues #[1543](https://github.com/certtools/intelmq/issues/1543)/

Ticket #[570](https://github.com/certtools/intelmq/issues/570) clearly lays out the need for a simplified configuration for IntelMQ 3.0.
The new configuration shall:

   * be on a per-program-basis (one config file per "bot"). The config files per program shall reside in $base/etc/config.d/ and follow the common linux standards.
   * the BOTS config file shall phase out (see #[1069](https://github.com/certtools/intelmq/issues/1069)). We won't need it. It's documentation or something which may reside in /usr/share/docs/intelmq or /var/lib/intelmq.
   * config language: JSON proved to be the wrong choice for representing complex configurations. We propose YAML.
   * support for variables (templating) in the config files. For example via Jina2. See #[1026](https://github.com/certtools/intelmq/issues/1026). Templating is a very relevant connection possibility between containers (and multiple instances) and a config: variables may be passed via ENV vars and instantiated as a configuration.
   * rendering of templates / instantiating: ``intelmqctl config-render``: this shall create an instantiated template with the values of the variables
   * configtest: there shall be (as is the case with IntelMQ 2.x) a ``intelmqctl configtest`` check
   * converter: there shall be a converter between old and new config format.

Runtime graph:

  * there shall be a ``intelmq connectiontest`` check which checks if all programs are connected
  * there shall be a ``intelmq fieldcheck`` test which checks if all the fields needed "downstream" by a program are filled in "upstream"

### domain oriented workflows

Currently, as of IntelMQ 2.x we are mostly focussing on number based (i.e. IP addresses) based workflows. 
For example: IP address 1.2.3.4 was infected with malware of type XY at timestamp 1st of January 2020 00:00 UTC 
according to shadowserver.
This leaves out all the workflows which are name-based. This includes phishing URLs, screenshots of hacked (defaced) 
web pages, etc.
Name based workflows have slightly different requirements. 
The most notable difference is the question whom to contact. And in fact, this depends heavily on the type
of incident. Defacements should usually be sent to the domain owner. However, if it's mass-defacement (i.e. all 
domains on the same IP address have the same defacement), then probably it should be primarily sent to the hoster

For a detailed description of this problem, please refer to [RIPE-658](ftp://ftp.ripe.net/ripe/docs/ripe-658.pdf).

The main requirements for IntelMQ 3.0 for domain oriented workflows are:

  * possibility to interface a screenshotting service which offers a permalink URL to the screenshot (--> addition to the IDF). 
  See also issue #[1048](https://github.com/certtools/intelmq/issues/1048). 
  * verifier bot to check if a domain is still online issue #[1047].
  * verifier bot, if a website (still) contains a certain text
  * documentation on the contact email address lookups for domains: when to use which approach.
  * proper tldextraction (``import tldextract``) and splitting of fqdn, base domain name and tld.
  * new expert: which CERT is "responsible" for a TLD lookup 


# Community management and community support

IntelMQ was founded by Aaron Kaplan (CERT.at) and Tomas Lima (back then CERT.pt), with the first version of the 
IntelMQ manager written by Mauro Silva (also back then CERT.pt).

Over the years IntelMQ developed into a well known "brand"/standard for automatically (pre-)processing incident 
reports / IT security log lines. It is widely used (we estimate that at the time of this writing, there are 
at least 600 installations globally) and there is wide interest by the CSIRTs as well as SOCs community.
IntelMQ was **always** an open source, community project.

However, reality has shown us, that a lot of the maintenance was done exclusively at CERT.at by one single developer.
And he would not be unhappy about additional help and support.

We therefore propose the hand over the IntelMQ development to either an open source foundation for further development
or to strengthen the community and allow the community to have more of say for future IntelMQ versions.
Note that the community is diverse and it will not be enough to hand it over to the CSIRTs Networks Tooling Group, 
since this would be a closed group (and IntelMQ's developer and user base is bigger).
Another option would be to open up the [IHAP group](https://www.enisa.europa.eu/topics/csirt-cert-services/community-projects/incident-handling-automation) and hand over
IntelMQ development to the IHAP group.

In any case, officially handing over IntelMQ to a community with a strong community spirit will ensure the 
stable continuation of the project in the spirit of the common good for the CSIRTs.


We propose to hold a discussion on this topic on the IHAP list as well as the intelMQ users and -developers list and set a deadline
for the decision and then follow up with the decision.



# IntelMQ-programs - improvements

## General principles

Each IntelMQ program (or -daemon) shall:

  * have a self-test command which shall trigger a python unit test: ``$ intelmq-shadowserver-collector --self-test``. This functionality is bascially already there
  * have a self-update-db command, which shall pull any updates of reference databases in: ``$ intelmq-geoip-expert --self-update-db``. In most programs (except the experts, this will be a NOP).
  * all programs shall have specific configuration options for specifying input and output queues and input and output queue types (stdin/stdout, pipes, message queuing systems, etc.). In other words: each IntelMQ program may send and receive to different MQs, files, pipes, sockets etc.


## Collectors

Here we are already quite strong: we have lots of collectors (data importers). STIX 2.x is still missing.
Should we get bored, here is a wish list of inputs: https://github.com/certtools/intelmq/blob/develop/docs/Feeds-whishlist.md and a wishlist for bots: https://github.com/certtools/intelmq/milestone/7

## (New) Transcoders

(very optional) 

By default, JSON MUST be encoded in UTF-8 (see [RFC8259](https://tools.ietf.org/html/rfc8259)). However this does not automatically mean that 
everyone will follow the requirements and send data as UTF-8. 

This class of programs (bots) simply takes the data on its input side, transcodes it (e.g. utf-16 to latin1) and passes it on.

We might consider, making this a generic property of a parser. TBD.


## (New) Converters

(optional, since it's often already implemented in the parsers)

This class of programs (bots) simply converts one format to IDF and vice versa. Example: n6 to IDF.
This functionality mostly exists already. It's just that we are giving this functionality its own class.

Converters might be needed for handling different versions of the IDF. Or this might be done implicitly: if a IDF header is present, 
we can derive the IDF version. If it's not present, then it's an old DHO format.



## (New) Verifiers
(This is optional)

We COULD be adding the concept of verifiers: think of these as expert bots which can verify a claim made in the 
IDF event. Example: the event talks about a webserver having an outdated SSL setting (Poodle vuln for example): 
the verifier (if enabled) should be able to reach out to the server and confirm the claim. This may be the 
basis for some kind of confidence score for the claim made in the event.

## Parsers

Can mostly stay the same. Again, the general principle of librarize everything applies especially here.

## Experts

  * have the new ``--self-update-db`` feature.
  * experts will mostly profit from the possibility to be embedded in a microservice or for being used as a library.

## Output

  * Stronger (more built-in) support for Elastic Search will be implicitly available via the new IDF.
  * Better tested ELK support (--> build a scenario where sending to ELK is a CI/CD test which must be passed). TBD: check if this is already done.
  * Better support for Splunk out of the box (same as with ELK) since many especially large organisations use splunk a lot.
  * Cassandra output should be added  (very optional)
  * Generic CSV writer XXX see issue XYZ -> @sebix please add XXX



## Specific improvements

### Postgresql Output bot

The eventDB structure (especially the ``events`` table) initially closely reflected the  format of the DHO 
(i.e. the old format). However, with lots of data pouring in, this "flat" table which is basically a log file
slows down postgresql a lot. See also issue #[1516](https://github.com/certtools/intelmq/issues/1516).

We propose to 

  - restructure the events table: use the well established 3rd normal form.
  - create a migration script for existing installations
  - use VIEWS and similar SQL tools to do lookups for reference tables (3rd normal form)
  - use temporal partitioning to keep individual (sub-)tables small and therefore in RAM.



# Footnotes

1. <a name="fn1">1</a>: There are tricks to make unix pipes support arbitrary (directed acyclical) graphs. 
e.g. <code>tee >(process1) >(process2) ...</code>. But this easily gets quite complex.


