<!-- comment
   SPDX-FileCopyrightText: 2015-2023 Sebastian Wagner, Filip Pokorný
   SPDX-License-Identifier: AGPL-3.0-or-later
-->


# Bot Development

Here you should find everything you need to develop a new bot.

## Steps

1. Create appropriately placed and named python file.
2. Use correct parent class.
3. Code the functionality you want (with mixins, inheritance, etc).
4. Create appropriately placed test file.
5. Prepare code for testing your bot.
6. Add documentation for your bot.
7. Add changelog and news info.

## Layout Rules

```
intelmq/
  lib/
    bot.py
    cache.py
    message.py
    pipeline.py
    utils.py
  bots/
    collector/
      <bot name>/
            collector.py
    parser/
      <bot name>/
            parser.py
    expert/
      <bot name>/
            expert.py
    output/
      <bot name>/
            output.py
  etc/
    runtime.yaml
```

Assuming you want to create a bot for a new 'Abuse.ch' feed. It turns out that here it is necessary to create different
parsers for the respective kind of events (e.g. malicious URLs). Therefore, the usual hierarchy `intelmq/bots/parser/<FEED>/parser.py` would not be suitable because it is necessary to have more parsers for each Abuse.ch Feed. The solution is to use the same hierarchy with an additional "description" in the file name, separated by underscore. Also see the section *Directories and Files naming*.

Example (including the current ones):

```
/intelmq/bots/parser/abusech/parser_domain.py
/intelmq/bots/parser/abusech/parser_ip.py
/intelmq/bots/parser/abusech/parser_ransomware.py
/intelmq/bots/parser/abusech/parser_malicious_url.py
```

#### Directories Hierarchy on Default Installation

- Configuration Files Path: `/opt/intelmq/etc/`
- PID Files Path: `/opt/intelmq/var/run/`
- Logs Files and dumps Path: `/opt/intelmq/var/log/`
- Additional Bot Files Path, e.g. templates or databases:
  `/opt/intelmq/var/lib/bots/[bot-name]/`

#### Directories and Files naming

Any directory and file of IntelMQ has to follow the Directories and Files naming. Any file name or folder name has to:

- be represented with lowercase and in case of the name has multiple words, the spaces between them must be removed or replaced by underscores
- be self-explaining what the content contains.

In the bot directories name, the name must correspond to the feed provider. If necessary and applicable the feed name can and should be used as postfix for the filename.

Examples:

```
intelmq/bots/parser/taichung/parser.py
intelmq/bots/parser/cymru/parser_full_bogons.py
intelmq/bots/parser/abusech/parser_ransomware.py
```


## Guide

### Naming your bot class

Class name of the bot (ex: PhishTank Parser) must correspond to the type of the bot (ex: Parser)
e.g. `PhishTankParserBot`

### Choosing the parent class

Please use the correct bot type as parent class for your bot. The `intelmq.lib.bot` module contains the following classes:

- `CollectorBot`
- `ParserBot`
- `ExpertBot`
- `OutputBot`

### Template

Please adjust the doc strings accordingly and remove the in-line comments (`#`).

```python
"""
SPDX-FileCopyrightText: 2021 Your Name
SPDX-License-Identifier: AGPL-3.0-or-later

Parse data from example.com, be a nice ExampleParserBot.

Document possible necessary configurations.
"""
import sys

# imports for additional libraries and intelmq
from intelmq.lib.bot import ParserBot


class ExampleParserBot(ParserBot):
    option1: str = "defaultvalue"
    option2: bool = False

    def process(self):
        report = self.receive_message()

        event = self.new_event(report)  # copies feed.name, time.observation
        ...  # implement the logic here
        event.add('source.ip', '127.0.0.1')
        event.add('extra', {"os.name": "Linux"})
        if self.option2:
            event.add('extra', {"customvalue": self.option1})

        self.send_message(event)
        self.acknowledge_message()


BOT = ExampleParserBot
```

Any attributes of the bot that are not private can be set by the user using the IntelMQ configuration settings.

There are some names with special meaning. These can be used i.e. called:

- `stop`: Shuts the bot down.
- `receive_message`
- `send_message`
- `acknowledge_message`: see next section
- `start`: internal method to run the bot

These can be defined:

- `init`: called at startup, use it to set up the bot (initializing classes, loading files etc)
- `process`: processes the messages
- `shutdown`: To Gracefully stop the bot, e.g. terminate connections

All other names can be used freely.

### Mixins

For common settings and methods you can use mixins from
`intelmq.lib.mixins`. To use the mixins, just let your bot inherit from the Mixin class (in addition to the inheritance
from the Bot class). For example:

```python
class HTTPCollectorBot(CollectorBot, HttpMixin):
```

The following mixins are available:

- `HttpMixin`
- `SqlMixin`
- `CacheMixin`

The `HttpMixin` provides the HTTP attributes described in `common-parameters` and the following methods:

- `http_get` takes an URL as argument. Any other arguments get passed to the `request.Session.get` method. `http_get`
  returns a
  `requests.Response`.
- `http_session` can be used if you ever want to work with the session object directly. It takes no arguments and
  returns the bots request.Session.

The `SqlMixin` provides methods to connect to SQL servers. Inherit this Mixin so that it handles DB connection for you.
You do not have to bother:

- connecting database in the `self.init()` method, self.cur will be set in the `__init__()`
- catching exceptions, just call `self.execute()` instead of
  `self.cur.execute()`
- `self.format_char` will be set to '%s' in PostgreSQL and to '?' in SQLite

The `CacheMixin` provides methods to cache values for bots in a Redis database. It uses the following attributes:

- `redis_cache_host: str = "127.0.0.1"`
- `redis_cache_port: int = 6379`
- `redis_cache_db: int = 9`
- `redis_cache_ttl: int = 15`
- `redis_cache_password: Optional[str] = None`

and provides the methods:

- `cache_exists`
- `cache_get`
- `cache_set`
- `cache_flush`
- `cache_get_redis_instance`

### Pipeline Interactions

We can call three methods related to the pipeline:

- `self.receive_message()`: The pipeline handler pops one message
    from the internal queue if possible. Otherwise one message from
    the sources list is popped, and added it to an internal queue. In
    case of errors in process handling, the message can still be found
    in the internal queue and is not lost. The bot class unravels the
    message a creates an instance of the Event or Report class.
- `self.send_message(event, path="_default")`: Processed
    message is sent to destination queues. It is possible to change
    the destination queues by optional `path` parameter.
- `self.acknowledge_message()`: Message formerly received by
    `receive_message` is removed from the internal
    queue. This should always be done after processing and after the
    sending of the new message. In case of errors, this function is
    not called and the message will stay in the internal queue waiting
    to be processed again.

### Logging

##### Log Messages Format

Log messages have to be clear and well formatted. The format is the following:

Format:

```
<timestamp> - <bot id> - <log level> - <log message>
```

Rules:

- the Log message MUST follow the common rules of a sentence, beginning with uppercase and ending with period.
- the sentence MUST describe the problem or has useful information to give to an inexperienced user a context. Pure stack traces without any further explanation are not helpful.

When the logger instance is created, the bot id must be given as parameter anyway. The function call defines the log level, see below.

##### Log Levels

- *debug*: Debugging information includes retrieved and sent messages, detailed status information. Can include
  sensitive information like passwords and amount can be huge.
- *info*: Logs include loaded databases, fetched reports or waiting messages.
- *warning*: Unexpected, but handled behavior.
- *error*: Errors and Exceptions.
- *critical* Program is failing.

##### What to Log

- Try to keep a balance between obscuring the source code file with hundreds of log messages and having too little log
  messages.
- In general, a bot MUST report error conditions.

##### How to Log

The Bot class creates a logger with that should be used by bots. Other components won't log anyway currently. Examples:

```python
self.logger.info('Bot start processing.')
self.logger.error('Pipeline failed.')
self.logger.exception('Pipeline failed.')
```

The `exception` method automatically appends an exception traceback. The logger instance writes by default to the file
`/opt/intelmq/var/log/[bot-id].log` and to stderr.

###### String formatting in Logs

Parameters for string formatting are better passed as argument to the log function, see
<https://docs.python.org/3/library/logging.html#logging.Logger.debug> In case of formatting problems, the error messages
will be better. For example:

```python
self.logger.debug('Connecting to %r.', host)
```

### Error handling

The bot class itself has error handling implemented. The bot itself is allowed to throw exceptions and **intended to fail**! The bot should fail in case of malicious messages, and in case of unavailable but necessary resources. The bot class handles the exception and will restart until the maximum number of tries is reached and fail then. Additionally, the message in question is dumped to the file `/opt/intelmq/var/log/[bot-id].dump` and removed from the queue.

### Initialization

Maybe it is necessary so setup a Cache instance or load a file into memory. Use the `init` function for this purpose:

```python
class ExampleParserBot(Bot):
    def init(self):
        try:
            self.database = pyasn.pyasn(self.database)
        except IOError:
            self.logger.error("pyasn data file does not exist or could not be "
                              "accessed in '%s'." % self.database)
            self.logger.error("Read 'bots/experts/asn_lookup/README.md' and "
                              "follow the procedure.")
            self.stop()
```

### Custom configuration checks

Every bot can define a static method `check(parameters)` which will be called by `intelmqctl check`. For example the check function of the ASNLookupExpert:

```python
@staticmethod
def check(parameters):
    if not os.path.exists(parameters.get('database', '')):
        return [["error", "File given as parameter 'database' does not exist."]]
    try:
        pyasn.pyasn(parameters['database'])
    except Exception as exc:
        return [["error", "Error reading database: %r." % exc]]
```

### Running

You can always start any bot directly from command line by calling the executable. The executable will be created during installation a directory for binaries. After adding new bots to the code, install IntelMQ to get the files created. Don't forget to give an bot id as first argument. Also, running bots with other users than `intelmq` will raise permission errors.

```bash
$ sudo -i intelmq
$ intelmqctl run file-output  # if configured
$ intelmq.bots.outputs.file.output file-output
```

You will get all logging outputs directly on stderr as well as in the log file.

### Examples

- Check [Expert Bots](https://github.com/certtools/intelmq/tree/develop/intelmq/bots/experts)
- Check [Parser Bots](https://github.com/certtools/intelmq/tree/develop/intelmq/bots/parsers)

### Parsers

Parsers can use a different, specialized Bot-class. It allows to work on individual elements of a report, splitting the functionality of the parser into multiple functions:

- `process`: getting and sending data, handling of failures etc.
- `parse`: Parses the report and splits it into single elements (e.g. lines). Can be overridden.
- `parse_line`: Parses elements, returns an Event. Can be overridden.
- `recover_line`: In case of failures and for the field `raw`, this function recovers a fully functional report containing only one element. Can be overridden.

For common cases, like CSV, existing function can be used, reducing the amount of code to implement. In the best case, only `parse_line` needs to be coded, as only this part interprets the data.

You can have a look at the implementation `intelmq/lib/bot.py` or at examples, e.g. the DummyBot in `intelmq/tests/lib/test_parser_bot.py`. This is a stub for creating a new Parser, showing the parameters and possible code:

```python
class MyParserBot(ParserBot):

    def parse(self, report):
        """A generator yielding the single elements of the data.

        Comments, headers etc. can be processed here. Data needed by
        `self.parse_line` can be saved in `self.tempdata` (list).

        Default parser yields stripped lines.
        Override for your use or use an existing parser, e.g.:
            parse = ParserBot.parse_csv
        """
        for line in utils.base64_decode(report.get("raw")).splitlines():
            yield line.strip()

    def parse_line(self, line, report):
        """A generator which can yield one or more messages contained in line.

        Report has the full message, thus you can access some metadata.
        Override for your use.
        """
        raise NotImplementedError

    def process(self):
        self.tempdata = []  # temporary data for parse, parse_line and recover_line
        self.__failed = []
        report = self.receive_message()

        for line in self.parse(report):
            if not line:
                continue
            try:
                # filter out None
                events = list(filter(bool, self.parse_line(line, report)))
            except Exception as exc:
                self.logger.exception('Failed to parse line.')
                self.__failed.append((exc, line))
            else:
                self.send_message(*events)

        for exc, line in self.__failed:
            self._dump_message(exc, self.recover_line(line))

        self.acknowledge_message()

    def recover_line(self, line):
        """Reverse of parse for single lines.

        Recovers a fully functional report with only the problematic line.
        """
        return 'n'.join(self.tempdata + [line])


BOT = MyParserBot
```

##### parse_line

One line can lead to multiple events, thus `parse_line` can't just return one Event. Thus, this function is a generator, which allows to easily return multiple values. Use `yield event` for valid Events and `return` in case of a void result (not parsable line, invalid data etc.).

### Tests

In order to do automated tests on the bot, it is necessary to write tests including sample data. Have a look at some existing tests:

- The DummyParserBot in `intelmq/tests/lib/test_parser_bot.py`. This test has the example data (report and event) inside the file, defined as dictionary.
- The parser for malwaregroup at `intelmq/tests/bots/parsers/malwaregroup/test_parser_*.py`. The latter loads a sample HTML file from the same directory, which is the raw report.
- The test for ASNLookupExpertBot has two event tests, one is an expected fail (IPv6).

Ideally an example contains not only the ideal case which should succeed, but also a case where should fail instead. (TODO: Implement assertEventNotEqual or assertEventNotcontainsSubset or similar) Most existing bots are only tested with one message. For newly written test it is appreciable to have tests including more then one message, e.g. a parser fed with an report consisting of multiple events.

```python
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.exampleparser.parser import ExampleParserBot  # adjust bot class name and module


class TestExampleParserBot(test.BotTestCase, unittest.TestCase):  # adjust test class name
    """A TestCase for ExampleParserBot."""

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ExampleParserBot  # adjust bot class name
        cls.default_input_message = EXAMPLE_EVENT  # adjust source of the example event (dict), by default an empty event or report (depending on bot type)

    # This is an example how to test the log output
    def test_log_test_line(self):
        """Test if bot does log example message."""
        self.run_bot()
        self.assertRegexpMatches(self.loglines_buffer,
                                 "INFO - Lorem ipsum dolor sit amet")

    def test_event(self):
        """Test if correct Event has been produced."""
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_REPORT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
```

When calling the file directly, only the tests in this file for the bot will be expected. Some default tests are always executed (via the `test.BotTestCase` class), such as pipeline and message checks, logging, bot naming or empty message handling.

See the `testing` section about how to run the tests.

### Cache

Bots can use a Redis database as cache instance. Use the `intelmq.lib.utils.Cache` class to set this up and/or look at existing bots, like the `cymru_whois` expert how the cache can be used. Bots must set a TTL for all keys that are cached to avoid caches growing endless over time. Bots must use the Redis databases >= 10, but not those already used by other bots. Look at `find intelmq -type f -name '*.py' -exec grep -r 'redis_cache_db' {} +` to see which databases are already used.

The databases < 10 are reserved for the IntelMQ core:

- 2: pipeline
- 3: statistics
- 4: tests

### Documentation

Please document your added/modified code.

For doc strings, we are using the
[sphinx-napoleon-google-type-annotation](http://www.sphinx-doc.org/en/stable/ext/napoleon.html#type-annotations).

Additionally, Python's type hints/annotations are used, see PEP484.


## Testing Pre-releases

### Installation

The installation procedures need to be adapted only a little bit.

For native packages, you can find the unstable packages of the next version
here: [Installation Unstable Native Packages](https://software.opensuse.org/download.html?project=home%3Asebix%3Aintelmq%3Aunstable&package=intelmq)
. The unstable only has a limited set of packages, so enabling the stable repository can be activated in parallel. For
CentOS 8 unstable, the stable repository is required.

For the installation with pip, use the `--pre` parameter as shown here following command:

```bash
pip3 install --pre intelmq
```

All other steps are not different. Please report any issues you find in
our [Issue Tracker](https://github.com/certtools/intelmq/issues/new).
