..
   SPDX-FileCopyrightText: 2023 Bundesamt für Sicherheit in der Informationstechnik (BSI)
   SPDX-License-Identifier: AGPL-3.0-or-later

##########################
Running IntelMQ as Library
##########################

.. contents::

************
Introduction
************

The feature is specified in `IEP007 <https://github.com/certtools/ieps/tree/iep-007/007/>`_.

**********
Quickstart
**********

First, import the Python module and a helper. More about the ``BotLibSettings`` later.

.. code-block:: python

   from intelmq.lib.bot import BotLibSettings
   from intelmq.bots.experts.domain_suffix.expert import DomainSuffixExpertBot

Then we need to initialize the bot's instance.
We pass two parameters:
* ``bot_id``: The id of the bot
* ``settings``: A Python dictionary of runtime configuration parameters, see :ref:`runtime-configuration`.
  The bot first loads the runtime configuration file if it exists.
  Then we update them with the ``BotLibSettings`` which are some accumulated settings disabling the logging to files and configure the pipeline so that we can send and receive messages directly to/from the bot.
  Last by not least, the actual bot parameters, taking the highest priority.

.. code-block:: python

   domain_suffix = DomainSuffixExpertBot('domain-suffix',  # bot id
                                         settings=BotLibSettings | {
                                                  'field': 'fqdn',
                                                  'suffix_file': '/usr/share/publicsuffix/public_suffix_list.dat'}

As the bot is not fully initialized, we can process messages now.
Inserting a message as dictionary:

.. code-block:: python

   queues = domain_suffix.process_message({'source.fqdn': 'www.example.com'})

The return value is a dictionary of queues, e.g. the output queue and the error queue.
More details below.

The methods accepts multiple messages as positional argument:

.. code-block:: python

   domain_suffix.process_message({'source.fqdn': 'www.example.com'}, {'source.fqdn': 'www.example.net'})
   domain_suffix.process_message(*[{'source.fqdn': 'www.example.com'}, {'source.fqdn': 'www.example.net'}])


Select the output queue (as defined in `destination_queues`), first message, access the field 'source.domain_suffix':

.. code-block:: python

   >>> output['output'][0]['source.domain_suffix']
   'com'

*************
Configuration
*************

Configuration files are not required to run IntelMQ as library.
Contrary to IntelMQ normal behavior, if the files ``runtime.yaml`` and ``harmonization.conf`` do not exist, IntelMQ won't raise any errors.
For the harmonization configuration, internal defaults are loaded.
