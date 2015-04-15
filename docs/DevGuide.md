# IntelMQ Developer Guide

**Table of Contents**

1. [Code and Repository Rules](#code-and-repository-rules)
2. [System Overview](#system-overview)
3. [Bot Developer Guide](#bot-developer-guide)

<a name="code-and-repository-rules"></a>
## Code and Repository Rules

This "Code and Repository Rules" section lays out the rules which developers of intelmq ahder to.
The purpose of this section is to clearly describe common coding styles and similar 
rules for IntelMQ.

### Goals

It is important, that developers agree and stick to these meta-guidelines. We expect you to
always try to:

* reduce the complexity of system administration
* reduce the complexity of writing new bots for new data feeds
* make your code easily and pleasantly readable
* reduce the probability of events lost in all process with persistence functionality (even system crash)
* strictly adher to the existing [Data Harmonization Ontology](https://github.com/certtools/intelmq/blob/master/docs/DataHarmonization.md) for key-values in events
* always use JSON format for all messages internally
* help and support the interconnection between IntelMQ and existing tools like AbuseHelper, CIF, etc. or new tools (in other words: we will not accept data-silos!)
* provide an easy way to store data into Log Collectors like ElasticSearch, Splunk
* provide an easy way to create your own black-lists
* provide easy to understand interfaces with other systems via HTTP RESTFUL API

The main take away point from the list above is: things **MUST** stay __intuitive__ and __easy__.
How do you test if things are easy? Let them new programers test-drive your features and if it is not understandable in 15 minutes, go back to the drawing board.

Similarly, if code does not get accepted upstream by the main developers, it is usually only because of the ease-of-use argument. Do not give up , go back to the drawing board, and re-submit again.


### Coding-Rules

In general, we follow the [Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/).
We recommend reading it before commiting code.

#### Identation

Identation of the code must done using 4 spaces for each level of identation.

#### Variable Names

* name of variables MUST be clear, easy to understand and reasonably short;
* it's not allowed to use acronyms which could be mistaken for a different word.

###### Example 1

Unclear variable name:
```
def process_line(self, evt):
```
Clear variable name:
```
def process_line(self, event):
```

Here, event is a short name, it is clear what it means (--> see Data Harmonisation Ontology) and better than ```evt```. 

###### Example 2

Unclear variable name:
```
n_evt = evt.deep_copy()
```
Clear variable name:
```
local_event = event.deep_copy()
```

**Reference:** [Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)

#### Event Harmonization

Any component of IntelMQ MUST respect the "Data Harmonization Ontology".

**Reference:** IntelMQ Data Harmonization - https://github.com/certtools/intelmq/blob/master/docs/DataHarmonization.md


#### Directory layout in the repository
```
intelmq\
  bin\
    intelmqctl
  lib\
    bot.py
    cache.py
    message.py
    pipeline.py
    utils.py
  bots\
    collector\
      <bot name>\
		    collector.py
    parser\
      <bot name>\
		    parser.py
    expert\
      <bot name>\
		    expert.py
    output\
      <bot name>\
		    output.py
    BOTS
  \conf
    pipeline.conf
    runtime.conf
    startup.conf
    system.conf
```
Note: assuming you want to create a bot for 'Abuse.ch Zeus' feed . But it turns out that here it is necessary to create different parsers for the respective kind of events (C&C, Binaries, Dropzones). Therefore, the hierarchy ‘intelmq\bots\parser\abusech\parser.py’ would not be suitable because it is necessary to have more parsers, as mentioned above. The solution is to use the same hierarchy with an additional "description" in the file name, separated by underscore. For better understanding, see the topic "Directories and Files Harmonization" on this page. 

Example:
```
\intelmq\bots\parser\abusech\parser_zeus_cc.py
\intelmq\bots\parser\abusech\parser_zeus_binaries.py
\intelmq\bots\parser\abusech\parser_zeus_dropzones.py
```


#### Directories Hierarchy on Default Installation

Configuration Files Path:
```
/opt/intelmq/etc/
```

PID Files Path:
```
/opt/intelmq/var/run/
```

Logs Files Path:
```
/opt/intelmq/var/log/
````

Additional Bot Files Path:
```
/opt/intelmq/var/lib/bots/
````

#### Directories and Files Harmonization

Any directory and file of IntelMQ **MUST** respect the "Directories and Files Harmonization". Any file name or folder name **MUST**:
* be represented with uppercase and in case of the name has multiple words, the spaces between them must be replaced by underscores;
* be self explained of the folder or file content;

In the bot directories name, the name **MUST** correspond to the feed name. If necessary, some words can be added to give context by joining together using underscores.

Example (without context words):
```
intelmq/bots/parser/dragonresearchgroup
intelmq/bots/parser/malwaredomainlist
```

Example (with context words):
```
intelmq/bots/parser/cymru_full_bogons
intelmq/bots/parser/taichung_city_netflow
```


#### Directories and  hard-coded file paths

Any directory or  hard-coded file path **MUST** correspond to the IntelMQ default directories or files, following the "Directories Hierarchy on Default Installation".

Example (intelmq/lib/bot.py):
```
import re
import sys
import json
import time
import ConfigParser

SYSTEM_CONF_FILE = "/opt/intelmq/etc/system.conf"
PIPELINE_CONF_FILE = "/opt/intelmq/etc/pipeline.conf"
RUNTIME_CONF_FILE = "/opt/intelmq/etc/runtime.conf"
DEFAULT_LOGGING_PATH = "/opt/intelmq/var/log/"

class Bot(object):

	def __init__(self):
		self.message_counter = 0
		self.check_bot_id(bot_id)
```

#### Licence and Author files

License and Authors files can be found at the root of repository.
* License file **MUST NOT** be modified except by the explicit written permission by CNCS/CERT.PT or CERT.at
* Credit to the authors file must be always retained. When a new contributor (person and/or organization) improves in some way the repository content (code or documentation), he or she might add his name to the list of contributors.

Note: license and authors MUST be only listed in an external file but not inside the code files.

#### Useless Code

Code that is not being use (code that are as comment) or deprecated, **MUST** be removed from the main repository in order to keep the number of lines of code (LoCs) small.

#### Log Messages Format

Log messages **MUST** be clear and well formatted. The format is the following:

Format:
```
<Timestamp> - <Name of bot> - <Level> - <Log message>
```

Rules:
* the Log message MUST follow the common rules of a sentence, beginning with uppercase and ending with period.
* the sentence MUST describe the problem or has useful information to give to an unexperienced user a context. Pure stack traces without any further explanation are not helpful.

#### What to log?
* Try to keep a balance between obscuring the source code file with hundreds of log messages and having too little log messages. 
* In general, a bot MUST report error conditions.

#### Unicode

* Each internal object in IntelMQ (Event, Report, etc) that has strings, their strings MUST be in UTF-8 unicode format.
* Any data received from external sources MUST be transformed into UTF-8 unicode format before add it to IntelMQ objects.

#### Class Names

Class name of the bot (ex: PhishTank Parser) must correspond to the type of the bot (ex: Parser). Example:

```
    class Expert(Bot):
        ....
        
    if __name__ == "__main__":
        bot = Expert(sys.argv[1])
        bot.start()
```    

#### Coding style

Any component of IntelMQ must follow the [Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/).

```
# pip install pep8
# pep8 --show-source <filename>.py
```

#### Back-end independence

Any component of the IntelMQ MUST be independent of the message queue technology (Redis, RabbitMQ, etc...), except 'lib/pipeline.py'. Intelmq bots MAY only assume to use the class specified in 'lib/pipeline.py' for inter-process or inter-bot communications.

#### Compatibility

IntelMQ core (including intelmqctl) MUST be compatible with IntelMQ Manager, IntelMQ UI and IntelMQ Mailer.




<a name="system-overview"></a>
## System Overview


### Main Components
Redis is used as:
* message queue for pipeline
* memcache for bots


### Code Architecture

![Code Architecture](http://s28.postimg.org/5wmak1upp/intelmq_arch_schema.png)


<a name="bot-developer-guide"></a>
## Bot Developer Guide

### Template

```
from intelmq.lib.bot import Bot, sys
from intelmq.lib.event import Event
from intelmq.bots import utils

class ExampleBot(Bot):

    def process(self):
        
        # get message from source queue in pipeline
        message = self.receive_message()

        # ------
        # write the code here to process the message
        # ------
                
        # send message to destination queue in pipeline
        self.send_message(new_message)

        # acknowledge message received to source queue in pipeline
        self.acknowledge_message()

if __name__ == "__main__":
    bot = ExampleBot(sys.argv[1])
    bot.start()
```

**Examples**

* Check [taxonomy](https://github.com/certtools/intelmq/blob/master/intelmq/bots/experts/taxonomy/taxonomy.py) expert bot
* Check [arbor](https://github.com/certtools/intelmq/blob/master/intelmq/bots/parsers/arbor/parser.py) parser bot

### Configure IntelMQ

In the end, the new information about the new bot should be added to BOTS file located at intelmq/intelmq/bots on repository.
