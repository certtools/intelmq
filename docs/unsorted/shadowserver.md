<!-- comment
   SPDX-FileCopyrightText: 2015-2023 Sebastian Wagner, Filip Pokorný
   SPDX-License-Identifier: AGPL-3.0-or-later
-->


# Shadowserver Parser

**Structure of this Parser Bot**

The parser consists of two files:

: - `_config.py`

- `parser.py` or `parser_json.py`

Both files are required for the parser to work properly.

**Add new Feedformats**

Add a new feed format and conversions if required to the file
`_config.py`. Don't forget to update the `mapping` dict. It is required to look up the correct configuration.

Look at the documentation in the bot's `_config.py` file for more information.
