<!--
SPDX-FileCopyrightText: 2017 Sebastian Wagner

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Common cron jobs for IntelMQ

Downloads the latest database files for commonly used bots.

To use the scripts, add them to the crontab of the user intelmq using
`crontab -e` (append `-u intelmq` if you are not logged in as intelmq) like this:

    02  01 *   *   *     intelmq.bots.experts.tor_nodes.expert --update-database

This will automatically update the database file for all bots of specified type (e.g. `tor_nodes`) and reloads the bots.

Or use the template in `intelmq-update-database` moving it to `/etc/cron.d/` and
adapting it as needed.

## Path

If your executables are in `/usr/bin/local/`, make sure this path is in the PATH of cron. You can add it by a line like this in your local crontab file:

```
PATH=/bin:/usr/bin:/usr/local/bin
```

Otherwise `intelmqctl` can't find the executables' paths and check if they are running correctly.

### Notes

* GeoLite2 City database is updated weekly, every Tuesday. No need to run the cron more often.
([source](https://support.maxmind.com/geoip-faq/geoip2-and-geoip-legacy-database-updates/how-often-are-the-geoip2-and-geoip-legacy-databases-updated/))

* ASN Lookup database is updated every two hours.
