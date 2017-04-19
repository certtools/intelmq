# File-Collector

This bot is capable of reading files from the local file-system.
This is handy for testing purposes, or when you need to react to spontaneous
events. In combination with the Generic CSV Parser this should work great.

## Parameters:

You can set four parameters:
 1. `path`: The path were your files are stored
 2. `postfix`: The postfix or a File-Extension of your file (e.g. `.csv`)
 3. `delete_file`: If this parameter is not empty, the found files will be deleted.
 4. `feed`: The name of the feed.

## Workflow:

The bot loops over all files in `path` and tests if their file name matches
*postfix, e.g. `*.csv`. If yes, the file will be read and inserted into the
queue.

If `delete_file` is set, the file will be deleted after processing. If deletion
is not possible, the bot will stop.

To prevent data loss, the bot also stops when no `postfix` is set and
`delete_file` was set. This can not be overridden.

The bot always sets the file name as feed.url
