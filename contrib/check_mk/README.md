<!--
SPDX-FileCopyrightText: 2019 Sebastian Wagner

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Monitoring scripts for check_mk

Some scripts to integrate IntelMQ into a [Check_MK](https://mathias-kettner.com/) instance:

To use the scripts, add them to the crontab of the user intelmq using
`crontab -e` (append `-u intelmq` if you are not logged in as intelmq):

```
*/1 * * * * /usr/local/bin/cronjob_intelmq_queues.py
*/1 * * * * /usr/local/bin/cronjob_intelmq_statistics.py
```

The spool directory used is `/var/lib/check_mk_agent/spool/`.

## Queues

This script queries all queues and writes the data to a `intelmq-queues` check.

## Statistics

This script queries the internal statistics (beta) and writes them to the `intelmq-statistics` check.
