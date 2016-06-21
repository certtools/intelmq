# Shadowserver-Parser Readme

## Structure of this Parser Bot:
The parser consists of two files:
 * config.py
 * parser.py

Both files are required for the parser to work properly.


## How to use the Parser:
Add the Shadowserver parser to your Botnet.

**Parameters**
 * feedname: The Name of the feed
 * feedcode: A Codename for the feed
 * override: A switch, 0 or 1 deciding if the parse shall override information
   which was added by a preceding collector.

Set at least the parameter `feedname`. it is required to find the correct
configuration. If this parameter is not set or not correct, the bot fail!
Feed-names are the Names of the Shadowserver Format specification pages.
E.g. `Botnet-Drone-Hadoop` for the feed corresponding to:
https://www.shadowserver.org/wiki/pmwiki.php/Services/Botnet-Drone-Hadoop


## Add new Feedformats:
Add a new feedformat and conversions if required to the file
`config.py`. Don't forget to update the `feed_idx` dict.
It is required to look up the correct configuration.
