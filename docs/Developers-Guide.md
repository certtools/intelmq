**Table of Contents:**
- [Intended Audience](#intended-audience)
  - [Goals](#goals)
- [Development Environment](#development-environment)
  - [Installation](#installation)
  - [How to develop](#how-to-develop)
  - [Update](#update)
  - [Testing](#testing)
    - [Additional optional requirements](#additional-optional-requirements)
    - [Run the tests](#run-the-tests)
    - [Environment variables](#environment-variables)
    - [Configuration test files](#configuration-test-files)
- [Development Guidelines](#development-guidelines)
  - [Coding-Rules](#coding-rules)
    - [Unicode](#unicode)
    - [Back-end independence and Compatibility](#back-end-independence-and-compatibility)
  - [Layout Rules](#layout-rules)
    - [Documentation](#documentation)
    - [Directories Hierarchy on Default Installation](#directories-hierarchy-on-default-installation)
    - [Directories and Files naming](#directories-and-files-naming)
    - [Class Names](#class-names)
  - [Data Harmonization Rules](#data-harmonization-rules)
  - [Code Submission Rules](#code-submission-rules)
    - [Releases, Repositories and Branches](#releases-repositories-and-branches)
    - [Branching model](#branching-model)
    - [How to Contribute](#how-to-contribute)
    - [Workflow](#workflow)
    - [Commit Messages](#commit-messages)
    - [Prepare for Discussion in GitHub](#prepare-for-discussion-in-github)
  - [License and Author files](#license-and-author-files)
- [System Overview](#system-overview)
  - [Code Architecture](#code-architecture)
  - [Pipeline](#pipeline)
- [Bot Developer Guide](#bot-developer-guide)
  - [Template](#template)
- [imports for additional libraries and intelmq](#imports-for-additional-libraries-and-intelmq)
  - [Pipeline interactions](#pipeline-interactions)
  - [Logging](#logging)
    - [Log Messages Format](#log-messages-format)
    - [Log Levels](#log-levels)
    - [What to Log](#what-to-log)
    - [How to Log](#how-to-log)
      - [String formatting in Logs](#string-formatting-in-logs)
  - [Error handling](#error-handling)
  - [Initialization](#initialization)
  - [Custom configuration checks](#custom-configuration-checks)
  - [Examples](#examples)
  - [Parsers](#parsers)
    - [parse_line](#parse_line)
  - [Tests](#tests)
  - [Configuration](#configuration)
  - [Cache](#cache)
- [Feeds documentation](#feeds-documentation)
- [Testing Pre-releases](#testing-pre-releases)
  - [Installation](#installation)

# Intended Audience
This guide is for developers of IntelMQ. It explains the code architecture, coding guidelines as well as ways you can contribute code or documentation.
If you have not done so, please read the [User Guide](User-Guide.md) first.
Once you feel comfortable running IntelMQ with open source bots and you feel adventurous enough to contribute to the project, this guide is for you.
It does not matter if you are an experienced Python programmer or just a beginner. There are a lot of samples to help you out.

However, before we go into the details, it is important to observe and internalize some overall project goals.

## Goals

It is important, that all developers agree and stick to these meta-guidelines.
IntelMQ tries to:

* Be well tested. For developers this means, we expect you to write unit tests for bots. Every time.
* Reduce the complexity of system administration
* Reduce the complexity of writing new bots for new data feeds
* Make your code easily and pleasantly readable
* Reduce the probability of events lost in all process with persistence functionality (even system crash)
* Strictly adhere to the existing [Data Harmonization Ontology](Data-Harmonization.md) for key-values in events
* Always use JSON format for all messages internally
* Help and support the interconnection between IntelMQ and existing tools like AbuseHelper, CIF, etc. or new tools (in other words: we will not accept data-silos!)
* Provide an easy way to store data into Log Collectors like ElasticSearch, Splunk
* Provide an easy way to create your own black-lists
* Provide easy to understand interfaces with other systems via HTTP RESTFUL API

The main take away point from the list above is: things **MUST** stay __intuitive__ and __easy__.
How do you ultimately test if things are still easy? Let them new programmers test-drive your features and if it is not understandable in 15 minutes, go back to the drawing board.

Similarly, if code does not get accepted upstream by the main developers, it is usually only because of the ease-of-use argument. Do not give up , go back to the drawing board, and re-submit again.


# Development Environment

## Installation

Developers can create a fork repository of IntelMQ in order to commit the new code to this repository and then be able to do pull requests to the main repository. Otherwise you can just use the 'certtools' as username below.

The following instructions will use `pip3 -e`, which gives you a so called *editable* installation. No code is copied in the libraries directories, there's just a link to your code. However, configuration files still required to be moved to `/opt/intelmq` as the instructions show.

In this guide we use `/opt/dev_intelmq` as local repository copy. You can also use other directories as long as they are readable by other unprivileged users (e.g. home directories on Fedora can't be read by other users by default).
`/opt/intelmq` is used as root location for IntelMQ installations, this is IntelMQ's default for this installation method. This directory is used for configurations (`/opt/intelmq/etc`), local states (`/opt/intelmq/var/lib`) and logs (`/opt/intelmq/var/log`).

```bash
sudo -s

git clone https://github.com/<your username>/intelmq.git /opt/dev_intelmq
cd /opt/dev_intelmq

pip3 install -e .

useradd -d /opt/intelmq -U -s /bin/bash intelmq

mkdir /opt/intelmq
mkdir -p /opt/intelmq/var/lib/bots/file-output/
mkdir -p /opt/intelmq/var/log/

cp -R /opt/dev_intelmq/intelmq/etc /opt/intelmq/
cp -R /opt/dev_intelmq/intelmq/bots/BOTS /opt/intelmq/etc/

chmod -R 0770 /opt/intelmq
chown -R intelmq.intelmq /opt/intelmq
```

**Note:** please do not forget that configuration files, log files will be available on `/opt/intelmq`. However, if your development is somehow related to any configuration file, keep using `/opt/intelmq` and then, before commit, change the configurations files on `/opt/dev_intelmq/intelmq/etc/` with your changes on `/opt/intelmq/etc/`.


## How to develop

After you successfully setup your IntelMQ development environment, you can perform any development on any `.py` file on `/opt/dev_intelmq`. After you change, you can use the normal procedure to run the bots:

```bash
su - intelmq

intelmqctl start spamhaus-drop-collector

tail -f /opt/intelmq/var/log/spamhaus-drop-collector.log
```

You can also add new bots, creating the new `.py` file on the proper directory inside `cd /opt/dev_intelmq/intelmq`. However, your IntelMQ installation with pip3 needs to be updated. Please check the following section.


## Update

In case you developed a new bot, you need to update your current development installation. In order to do that, please follow this procedure:


1. Add the new bot information to `/opt/dev_intelmq/intelmq/bots/BOTS`, not `/opt/intelmq/etc/BOTS`.
2. Make sure that you have your new bot in the right place and the information on BOTS file is correct.
3. Execute the following commands:

```bash
sudo -s

cd /opt/dev_intelmq
pip3 install -e .
cp /opt/dev_intelmq/intelmq/bots/BOTS /opt/intelmq/etc/BOTS

chmod -R 0770 /opt/intelmq
chown -R intelmq.intelmq /opt/intelmq
```

Now you can test run your new bot following this procedure:

```bash
su - intelmq

intelmqctl start <bot_id>
```

## Testing

### Additional optional requirements

For the documentation tests two additional libraries are required: Cerberus and PyYAML. You can install them with pip:

```bash
pip3 install Cerberus PyYAML
```

or the package management of your operating system.

### Run the tests

All changes have to be tested and new contributions should be accompanied by according unit tests. You can run the tests by changing to the directory with IntelMQ repository and running either `unittest` or `nosetests`:

    cd /opt/dev_intelmq
    python3 -m unittest {discover|filename}  # or
    nosetests3 [filename]  # alternatively nosetests or nosetests-3.5 depending on your installation, or
    python3 setup.py test  # uses a build environment (no external dependencies)

It may be necessary to switch the user to `intelmq` if the run-path (`/opt/intelmq/var/run/`) is not writeable by the current user. Some bots need local databases to succeed. If you don't mind about those and only want to test one explicit test file, give the file path as argument.

There is a [Travis-CI](https://travis-ci.org/certtools/intelmq/builds) setup for automatic testing, which triggers on pull requests. You can also easily activate it for your forks.

### Environment variables

There are a bunch of environment variables which switch on/off some tests:

* `INTELMQ_TEST_DATABASES`: databases such as postgres, elasticsearch, mongodb are not tested by default, set to 1 to test those bots. These tests need preparation, e.g. running databases with users and certain passwords etc. Have a look at the `.travis.yml` in IntelMQ's repository for steps to set databases up.
* `INTELMQ_SKIP_INTERNET`: tests requiring internet connection will be skipped if this is set to 1.
* `INTELMQ_SKIP_REDIS`: redis-related tests are ran by default, set this to 1 to skip those.
* `INTELMQ_TEST_LOCAL_WEB`: tests which connect to local web servers or proxies are active when set to 1. Running these tests assume a local webserverserving certain files and/or proxy. Example preparation steps can be found in `.travis.yml` again.
* `INTELMQ_TEST_EXOTIC`: some bots and tests require libraries which may not be available, those are skipped by default. To run them, set this to 1.
* `INTELMQ_TEST_REDIS_PASSWORD`: Set this value to the password for the local redis database if needed.

For example, to run all tests you can use:

```bash
INTELMQ_TEST_DATABASES=1 INTELMQ_TEST_LOCAL_WEB=1 INTELMQ_TEST_EXOTIC=1 nosetests3
```

### Configuration test files

The tests use the configuration files in your working directory, not those installed in `/opt/intelmq/etc/` or `/etc/`.  You can run the tests for a locally changed intelmq without affecting an installation or
requiring root to run them.

# Development Guidelines

## Coding-Rules

Most important: **KEEP IT SIMPLE**!!
This can not be over-estimated. Feature creep can destroy any good software project. But if new folks can not understand what you wrote in 10-15 minutes, it is not good. It's not about the performance, etc. It's about readability.


In general, we follow the [Style Guide for Python Code (PEP8)](https://www.python.org/dev/peps/pep-0008/).
We recommend reading it before committing code.

There are some exceptions: sometimes it does not make sense to check for every PEP8 error (such as whitespace indentation when you want to make a dict=() assignment
look pretty. Therefore, we do have some exceptions defined in the `setup.cfg` file.

We support Python 3 only.

### Unicode

* Each internal object in IntelMQ (Event, Report, etc) that has strings, their strings MUST be in UTF-8 Unicode format.
* Any data received from external sources MUST be transformed into UTF-8 Unicode format before add it to IntelMQ objects.

### Back-end independence and Compatibility

Any component of the IntelMQ MUST be independent of the message queue technology (Redis, RabbitMQ, etc...).

## Layout Rules

```bash
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
    BOTS
  /conf
    pipeline.conf
    runtime.conf
    defaults.conf
```

Assuming you want to create a bot for a new 'Abuse.ch' feed. It turns out that here it is necessary to create different parsers for the respective kind of events (e.g. malicious URLs). Therefore, the usual hierarchy ‘intelmq/bots/parser/<FEED>/parser.py’ would not be suitable because it is necessary to have more parsers for each Abuse.ch Feed. The solution is to use the same hierarchy with an additional "description" in the file name, separated by underscore. Also see the section *Directories and Files naming*.

Example (including the current ones):
```
/intelmq/bots/parser/abusech/parser_domain.py
/intelmq/bots/parser/abusech/parser_ip.py
/intelmq/bots/parser/abusech/parser_ransomware.py

/intelmq/bots/parser/abusech/parser_malicious_url.py
```

### Documentation

Please document your added/modified code.

For doc strings, we are using the [sphinx-napoleon-google-type-annotation](http://www.sphinx-doc.org/en/stable/ext/napoleon.html#type-annotations).

Additionally, Python's type hints/annotations are used, see [PEP 484](https://www.python.org/dev/peps/pep-0484/).

### Directories Hierarchy on Default Installation

* Configuration Files Path: `/opt/intelmq/etc/`
* PID Files Path: `/opt/intelmq/var/run/`
* Logs Files and dumps Path: `/opt/intelmq/var/log/`
* Additional Bot Files Path, e.g. templates or databases: `/opt/intelmq/var/lib/bots/[bot-name]/`

### Directories and Files naming

Any directory and file of IntelMQ has to follow the Directories and Files naming. Any file name or folder name has to
* be represented with lowercase and in case of the name has multiple words, the spaces between them must be removed or replaced by underscores;
* be self-explaining what the content contains.

In the bot directories name, the name must correspond to the feed provider. If necessary and applicable the feed name can and should be used as postfix for the filename.

Examples:
```
intelmq/bots/parser/malwaredomainlist/parser.py
intelmq/bots/parser/taichung/parser.py
intelmq/bots/parser/cymru/parser_full_bogons.py
intelmq/bots/parser/abusech/parser_ransomware.py
```

### Class Names

Class name of the bot (ex: PhishTank Parser) must correspond to the type of the bot (ex: Parser) e.g. `PhishTankParserBot`


## Data Harmonization Rules

Any component of IntelMQ MUST respect the "Data Harmonization Ontology".

**Reference:** IntelMQ Data Harmonization - [Data Harmonization Ontology](Data-Harmonization.md)


## Code Submission Rules

### Releases, Repositories and Branches

  * The main repository is in [github.com/certtools/intelmq](https://github.com/certtools/intelmq).
  * There are a couple of forks which might be regularly merged into the main repository. They are independent and can have incompatible changes and can deviate from the upstream repository.
  * We use [semantic versioning](http://semver.org/). A short summary:
    * a.x are stable releases
    * a.b.x are bugfix/patch releases
    * a.x must be compatible to version a.0 (i.e. API/Config-compatibility)
  * If you contribute something, please fork the repository, create a separate branch and use this for pull requests, see section below.

### Branching model

  * "master" is the stable branch. It hold the latest stable release. Non-developers should only work on this branch. The recommended log level is WARNING. Code is only added by merges from the maintenance branches.
  * "maintenance/a.b.x" branches accumulate (cherry-picked) patches for a maintenance release (a.b.x). Recommended for experienced users which deploy intelmq themselves. No new features will be added to these branches.
  * "develop" is the development branch for the next stable release (a.x). New features must go there. Developers may want to work on this branch. This branch also holds all patches from maintenance releases if applicable. The recommended log level is DEBUG.
  * Separate branches to develop features or bug fixes may be used by any contributor.

### How to Contribute

  * Make separate pull requests / branches on GitHub for changes. This allows us to discuss things via GitHub.
  * We prefer one  Pull Request per feature or change. If you have a bunch of small fixes, please don't create one RP per fix :)
  * Only very small and changes (docs, ...) might be committed directly to development branches without Pull Request by the [core-team](https://github.com/orgs/certtools/teams/core).
  * Keep the balance between atomic commits and keeping the amount of commits per PR small. You can use interactive rebasing to squash multiple small commits into one (`rebase -i [base-branch]`). Only do rebasing if the code you are rebasing is yet not used by others or is already merged - because then others may need to run into conflicts.
  * Make sure your PR is merge able in the develop branch and all tests are successful.
  * If possible [sign your commits with GPG](https://help.github.com/articles/signing-commits-using-gpg/).

### Workflow

We assume here, that origin is your own fork. We first add the upstream repository:

```bash
> git remote add upstream https://github.com/certtools/intelmq.git
```

Syncing develop:

```bash
> git checkout develop
> git pull upstream develop
> git push origin develop
```
You can do the same with the branches `master` and `maintenance`.

Create a separate feature-branch to work on, sync develop with upstream. Create working branch from develop:
```bash
> git checkout develop
> git checkout -b bugfix
# your work
> git commit
```
Or, for bugfixes create a separate bugfix-branch to work on, sync maintenance with upstream. Create working branch from maintenance:
```bash
> git checkout maintenance
> git checkout -b new-feature
# your work
> git commit

Getting upstream's changes for master or any other branch:
```bash
> git checkout develop
> git pull upstream develop
> git push origin develop
```
There are 2 possibilities to get upstream's commits into your branch. Rebasing and Merging. Using rebasing, your history is rewritten, putting your changes on top of all other commits. You can use this if your changes are not published yet (or only in your fork).
```bash
> git checkout bugfix
> git rebase develop
```
Using the `-i` flag for rebase enables interactive rebasing. You can then remove, reorder and squash commits, rewrite commit messages, beginning with the given branch, e.g. develop.

Or using merging. This doesn't break the history. It's considered more , but also pollutes the history with merge commits.
```bash
> git checkout bugfix
> git merge develop
```

Also see the [development workflow of Scipy](https://docs.scipy.org/doc/numpy/dev/gitwash/development_workflow.html) which has more examples.

You can then create a PR with your branch `bugfix` to our upstream repository, using GitHub's web interface.

### Commit Messages

If it fixes an existing issue, please use GitHub syntax, e.g.: `fixes certtools/intelmq#<IssueID>`

### Prepare for Discussion in GitHub

If we don't discuss it, it's probably not tested.

## License and Author files

License and Authors files can be found at the root of repository.
* License file **MUST NOT** be modified except by the explicit written permission by CNCS/CERT.PT or CERT.at
* Credit to the authors file must be always retained. When a new contributor (person and/or organization) improves in some way the repository content (code or documentation), he or she might add his name to the list of contributors.

License and authors must be only listed in an external file but not inside the code files.


# System Overview

In the `intelmq/lib/` directory you can find some libraries:
 * Bots: Defines base structure for bots and handling of startup, stop, messages etc.
 * Cache: For some expert bots it does make sense to cache external lookup results. Redis is used here.
 * Harmonization: For defined types, checks and sanitation methods are implemented.
 * Message: Defines Events and Reports classes, uses harmonization to check validity of keys and values according to config.
 * Pipeline: Writes messages to message queues. Implemented for productions use is only Redis. A python-only solution is used by testing. A solution using ZMQ is in development.
 * Test: Base class for bot tests with predefined test and assert methods.
 * Utils: Utility functions used by system components.

## Code Architecture

![Code Architecture](images/intelmq-arch-schema.png)

## Pipeline

  * collector bot
  **TBD**


# Bot Developer Guide

There's a dummy bot including tests at `intelmq/tests/lib/test_parser_bot.py`.

You can always start any bot directly from command line by calling the executable.
The executable will be created during installation a directory for binaries. After adding new bots to the code, install IntelMQ to get the files created.
Don't forget to give an bot id as first argument. Also, running bots with other users than `intelmq` will raise permission errors.
```bash
$ sudo -i intelmq
$ intelmqctl run file-output  # if configured
$ intelmq.bots.outputs.file.output file-output
```
You will get all logging outputs directly on stderr as well as in the log file.

## Template
Please adjust the doc strings accordingly and remove the in-line comments (`#`).
```python
# -*- coding: utf-8 -*-
"""
ExampleParserBot parses data from example.com.

Document possible necessary configurations.
"""
from __future__ import unicode_literals
import sys

# imports for additional libraries and intelmq
from intelmq.lib.bot import Bot


class ExampleParserBot(Bot):
    def process(self):
        report = self.receive_message()

        event = self.new_event(report)  # copies feed.name, time.observation
        ... # implement the logic here
        event.add('source.ip', '127.0.0.1')
        event.add('extra', {"os.name": "Linux"})

        self.send_message(event)
        self.acknowledge_message()


BOT = ExampleParserBot
```

There are some names with special meaning. These can be used i.e. called:
* `stop`: Shuts the bot down.
* `receive_message`, `send_message`, `acknowledge_message`: see next section
* `parameters`: the bots configuration as object
* `start`: internal method to run the bot

These can be defined:
* `init`: called at startup, use it to set up the bot (initializing classes, loading files etc)
* `process`: processes the messages
* `shutdown`: To Gracefully stop the bot, e.g. terminate connections

All other names can be used freely.

## Pipeline interactions

We can call three methods related to the pipeline:

  - `self.receive_message()`: The pipeline handler pops one message from the internal queue if possible. Otherwise one message from the sources list is popped, and added it to an internal queue. In case of errors in process handling, the message can still be found in the internal queue and is not lost. The bot class unravels the message a creates an instance of the Event or Report class.
  - `self.send_message(event, path="_default")`: Processed message is sent to destination queues. It is possible to change the destination queues by optional `path` parameter.
  - `self.acknowledge_message()`: Message formerly received by `receive_message` is removed from the internal queue. This should always be done after processing and after the sending of the new message. In case of errors, this function is not called and the message will stay in the internal queue waiting to be processed again.

## Logging

### Log Messages Format

Log messages have to be clear and well formatted. The format is the following:

Format:
```
<timestamp> - <bot id> - <log level> - <log message>
```

Rules:
* the Log message MUST follow the common rules of a sentence, beginning with uppercase and ending with period.
* the sentence MUST describe the problem or has useful information to give to an inexperienced user a context. Pure stack traces without any further explanation are not helpful.

When the logger instance is created, the bot id must be given as parameter anyway. The function call defines the log level, see below.

### Log Levels

* *debug*: Debugging information includes retrieved and sent messages, detailed status information. Can include sensitive information like passwords and amount can be huge.
* *info*: Logs include loaded databases, fetched reports or waiting messages.
* *warning*: Unexpected, but handled behavior.
* *error*: Errors and Exceptions.
* *critical* Program is failing.

### What to Log

* Try to keep a balance between obscuring the source code file with hundreds of log messages and having too little log messages.
* In general, a bot MUST report error conditions.

### How to Log
The Bot class creates a logger with that should be used by bots. Other components won't log anyway currently. Examples:

```python
self.logger.info('Bot start processing.')
self.logger.error('Pipeline failed.')
self.logger.exception('Pipeline failed.')
```
The `exception` method automatically appends an exception traceback. The logger instance writes by default to the file `/opt/intelmq/var/log/[bot-id].log` and to stderr.

#### String formatting in Logs

Parameters for string formatting are better passed as argument to the log function, see https://docs.python.org/3/library/logging.html#logging.Logger.debug
In case of formatting problems, the error messages will be better. For example:

```python
self.logger.debug('Connecting to %r.', host)
```

## Error handling

The bot class itself has error handling implemented. The bot itself is allowed to throw exceptions and **intended to fail**! The bot should fail in case of malicious messages, and in case of unavailable but necessary resources. The bot class handles the exception and will restart until the maximum number of tries is reached and fail then. Additionally, the message in question is dumped to the file `/opt/intelmq/var/log/[bot-id].dump` and removed from the queue.

## Initialization

Maybe it is necessary so setup a Cache instance or load a file into memory. Use the `init` function for this purpose:

```python
class ExampleParserBot(Bot):
    def init(self):
        try:
            self.database = pyasn.pyasn(self.parameters.database)
        except IOError:
            self.logger.error("pyasn data file does not exist or could not be "
                              "accessed in '%s'." % self.parameters.database)
            self.logger.error("Read 'bots/experts/asn_lookup/README.md' and "
                              "follow the procedure.")
            self.stop()
```

## Custom configuration checks

Every bot can define a static method `check(parameters)` which will be called by `intelmqctl check`.
For example the check function of the ASNLookupExpert:

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

## Examples

* Check [Expert Bots](../intelmq/bots/experts/)
* Check [Parser Bots](../intelmq/bots/parsers/)

## Parsers

Parsers can use a different, specialized Bot-class. It allows to work on individual elements of a report, splitting the functionality of the parser into multiple functions:

 * `process`: getting and sending data, handling of failures etc.
 * `parse`: Parses the report and splits it into single elements (e.g. lines). Can be overridden.
 * `parse_line`: Parses elements, returns an Event. Can be overridden.
 * `recover_line`: In case of failures and for the field `raw`, this function recovers a fully functional report containing only one element. Can be overridden.

For common cases, like CSV, existing function can be used, reducing the amount of code to implement. In the best case, only `parse_line` needs to be coded, as only this part interprets the data.

You can have a look at the implementation `intelmq/lib/bot.py` or at examples, e.g. the DummyBot in `intelmq/tests/lib/test_parser_bot.py`. This is a stub for creating a new Parser, showing the parameters and possible code:

```python
class MyParserBot(ParserBot):

    def parse(self, report):
        """
        A generator yielding the single elements of the data.

        Comments, headers etc. can be processed here. Data needed by
        `self.parse_line` can be saved in `self.tempdata` (list).

        Default parser yields stripped lines.
        Override for your use or use an existing parser, e.g.:
            parse = ParserBot.parse_csv
        """
        for line in utils.base64_decode(report.get("raw")).splitlines():
            yield line.strip()

    def parse_line(self, line, report):
        """
        A generator which can yield one or more messages contained in line.

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
        """
        Reverse of parse for single lines.

        Recovers a fully functional report with only the problematic line.
        """
        return '\n'.join(self.tempdata + [line])


BOT = MyParserBot
```

### parse_line
One line can lead to multiple events, thus `parse_line` can't just return one Event. Thus, this function is a generator, which allows to easily return multiple values. Use `yield event` for valid Events and `return` in case of a void result (not parseable line, invalid data etc.).

## Tests

In order to do automated tests on the bot, it is necessary to write tests including sample data. Have a look at some existing tests:

 - The DummyParserBot in `intelmq/tests/lib/test_parser_bot.py`. This test has the example data (report and event) inside the file, defined as dictionary.
 - The parser for malwaregroup at `intelmq/tests/bots/parsers/malwaregroup/test_parser_*.py`. The latter loads a sample HTML file from the same directory, which is the raw report.
 - The test for ASNLookupExpertBot has two event tests, one is an expected fail (IPv6).

Ideally an example contains not only the ideal case which should succeed, but also a case where should fail instead. (TODO: Implement assertEventNotEqual or assertEventNotcontainsSubset or similar)
Most existing bots are only tested with one message. For newly written test it is appreciable to have tests including more then one message, e.g. a parser fed with an report consisting of multiple events.

```python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.exampleparser.parser import ExampleParserBot  # adjust bot class name and module


class TestExampleParserBot(test.BotTestCase, unittest.TestCase):  # adjust test class name
    """
    A TestCase for ExampleParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ExampleParserBot  # adjust bot class name
        cls.default_input_message = EXAMPLE_EVENT  # adjust source of the example event (dict), by default an empty event or report (depending on bot type)

    # This is an example how to test the log output
    def test_log_test_line(self):
        """ Test if bot does log example message. """
        self.run_bot()
        self.assertRegexpMatches(self.loglines_buffer,
                                 "INFO - Lorem ipsum dolor sit amet")

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_REPORT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
```

When calling the file directly, only the tests in this file for the bot will be expected. Some default tests are always executed (via the `test.BotTestCase` class), such as pipeline and message checks, logging, bot naming or empty message handling.

See the [testing section](#testing) about how to run the tests.

## Configuration

In the end, the new information about the new bot should be added to BOTS file
located at `intelmq/bots`. Note that the file is sorted!

## Cache

Bots can use a Redis database as cache instance. Use the `intelmq.lib.utils.Cache` class to set this up and/or look at existing bots, like the `cymru_whois` expert how the cache can be used.
Bots must set a TTL for all keys that are cached to avoid caches growing endless over time.
Bots must use the Redis databases `>=` 10, but not those already used by other bots. See `bots/BOTS` what databases are already used.

The databases `<` 10 are reserved for the IntelMQ core:
 * 2: pipeline
 * 4: tests

# Feeds documentation

The feeds which are known to be working with IntelMQ are documented in the machine-readable file `intelmq/etc/feeds.yaml`. The human-readable documentation is in `docs/Feeds.md`. In order to keep these files in sync, call `intelmq/bin/intelmq_gen_docs.py` which generates the Markdown file from the YAML file.

So to add a new feeds, change the `feeds.yaml` and then call the `intelmq_gen_docs.py` file.

# Testing Pre-releases

## Installation

The [installation procedures](Install.md) needs to be adapted only a little bit.

For native packages, you can find the unstable packages of the next version here: [Installation Unstable Native Packages](https://software.opensuse.org/download.html?project=home%3Asebix%3Aintelmq%3Aunstable&package=intelmq).

For the installation with pip, use the `--pre` parameter as shown here following command:

```bash
pip3 install --pre intelmq
```

All other steps are not different. Please report any issues you find in our [Issue Tracker](https://github.com/certtools/intelmq/issues/new).
