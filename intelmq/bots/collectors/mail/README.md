# Mail collector bots

This file should contain the documentation for:

  * Generic Mail Attachment Fetcher
  * Generic Mail URL Fetcher

Currently, no documentation is available.


## Generic Mail URL Fetcher

### Chunking

For line-based inputs the bot can split up large reports into smaller chunks.

This is particularly important for setups that use Redis as a message queue
which has a per-message size limitation of 512 MB.

To configure chunking, set `chunk_size` to a value in bytes.
`chunk_replicate_header` determines whether the header line should be repeated
for each chunk that is passed on to a parser bot.

Specifically, to configure a large file input to work around Redis' size
limitation set `chunk_size` to something like `384000000`, i.e., ~384 MB.
