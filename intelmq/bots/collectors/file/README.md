# File-Collector

This bot is capable of reading files from the local file-system.
This is handy for testing purposes, or when you need to react to spontaneous
events. In combination with the Generic CSV Parser this should work great.

## Parameters:

You need to set these four parameters:
 1. `path`: The path were your files are stored
 2. `postfix`: The postfix or a File-Extension of your file (e.g. `.csv`)
 3. `delete_file`: If this parameter is not empty, the found files will be deleted.
 4. `feed`: The name of the feed.

## Chunking:

Additionally, for line-based inputs the bot can split up large reports into
smaller chunks.

This is particularly important for setups that use Redis as a message queue
which has a per-message size limitation of 512 MB.

To configure chunking, set `chunk_size` to a value in bytes.
`chunk_replicate_header` determines whether the header line should be repeated
for each chunk that is passed on to a parser bot.

Specifically, to configure a large file input to work around Redis' size
limitation set `chunk_size` to something like `384000`, i.e., ~384 MB.

## Workflow:

The bot loops over all files in `path` and tests if their file name matches
*postfix, e.g. `*.csv`. If yes, the file will be read and inserted into the
queue.

If `delete_file` is set, the file will be deleted after processing. If deletion
is not possible, the bot will stop.

To prevent data loss, the bot also stops when no `postfix` is set and
`delete_file` was set. This can not be overridden.

The bot always sets the file name as feed.url
