CHANGELOG
==========

## 2015/06/03 (aaron)

  * fixed the license to AGPL in setup.py
  * moved back the docs/* files from the wiki repo to docs/. See #205.
  * added python-zmq as a setup requirment in UserGuide . See #206




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
  - the harmonization.py has datatypes witch contains sanitize and validation methods that will make sure that the values are correct to be part of an event.



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



* Defaults configrations
  - new configuration file to specify the default parameters which will be apllied to all bots. Bots can overwrite the configurations.



* New bots/feeds
