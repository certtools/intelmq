CHANGELOG
==========

v1.0 (in development, master branch)
----

### General changes
- Dropped support for Python 2, Python >= 3.3 is needed
- Dropped startup.conf and system.conf. Sections in BOTS can be copied directly yo runtime.conf now.

### Bot changes
- ENH: added bots.collectors.rt.collector
- ENH: added bots.parsers.spamhaus.parser_cert
- ENH: added bots.parsers.fraunhofer.parser_dga
- ENH: added bots.experts.certat_contact.expert
- MAINT: renamed bots.parsers.spamhaus.parser to bots.parsers.spamhaus.parser_drop
- Dropped dragon research group feeds: discontinued
- changed configuration syntax for bots.experts.modify
- dropped bots.collectors.bitsight.collector in favor of bots.collectors.http.collector_http_stream

### Bug fixes
- FIX: all bots handle message which are None
- FIX: various encoding issues resolved in core and bots
- FIX: time.observation is generated in collectors, not in parsers

### Other enhancements and changes
- TST: testing framework for core and tests. Newly introduced components should always come with proper unit tests.
- ENH: intelmqctl has shortcut parameters and can clear queues
- STY: code obeys PEP8, new code should always be properly formatted
- ENH: More code is Python 3 compatible
- DOC: Updated user and dev guide
- Removed Message.contains, Message.update methods Message.add ignore parameter

###Configuration
- ENH: New parameter and field named accuracy to represent the accuracy of each feed
- Consistent naming "overwrite" to switch overwriting capabilities of bots (as opposed to override)
- Renamed http_ssl_proxy to https_proxy

### Harmonization
- ENH: Additional data types: integer, float and Boolean
- ENH: Added descriptions and matching types to all fields
- DOC: harmonization documentation has same fields as configuration, docs are generated from configuration
- ENH: New type LowercaseString and UppercaseString
- BUG: FQDNs are only allowed in IDN representation

#### Most important changes:
- `(source|destination).bgp_prefix` is now `(source|destination).network`
- `(source|destination).cc` is now `(source|destination).geolocation.cc`
- `(source|destination).reverse_domain_name` is `(source|destination).reverse_dns`
- `misp_id` changed to `misp_uuid`
- `protocol.transport` added
- `webshot_url` removed
- `additional_information` renamed to `extra`, must be JSON
- `os.name`, `os.version`, `user_agent` removed in favor of `extra`

-----



## 2015/06/03 (aaron)

  * fixed the license to AGPL in setup.py
  * moved back the docs/* files from the wiki repo to docs/. See #205.
  * added python-zmq as a setup requirement in UserGuide . See #206




## When did this happen? (XXX FIXME)

* improvements in pipeline
  FILE: lib/pipeline.py

  - PipelineFactory to give possibility to easily add a new broker (Redis, ZMQ, etc..)
  - Splitter feature: if this option is enable, will split the events in source queue to multiple destination queues



* add different messages support
  FILE: lib/message.py

  - the system is flexible to define a new type of message like 'tweet' without change anything in bot.py, pipeline.py. Just need to add a new class in message.py and harmonization.conf



* add harmonization support
  FILE: lib/harmonization.py
  FILE: conf/harmonization.conf

  - in harmonization.conf is possible to define the fields of a specific message in json format.
  - the harmonization.py has data types witch contains sanitize and validation methods that will make sure that the values are correct to be part of an event.



* Error Handling
  - multiple parameters in configuration which gives possibility to define how bot will handle some errors. Example of parameters:
  "error_procedure" - retry or pass in case of error
  "error_retry_delay" - time in seconds to retry
  "error_max_retries" - number of retries
  "error_log_message" - log or not the message in error log
  "error_log_exception" - log or not the exception in error log
  "error_dump_message" - log or not the message in dump log to be fixed and re-insert in pipeline



* Exceptions
  FILE: lib/exceptions.py

  - custom exceptions for IntelMQ



* Defaults configurations
  - new configuration file to specify the default parameters which will be applied to all bots. Bots can overwrite the configurations.



* New bots/feeds
