# Common cron jobs for intelmq

Downloads current lookup data for commonly used bots.

To use the scripts, add them to the crontab of the user intelmq using
`crontab -e` (append `-u intelmq` if you are not logged in as intelmq):

    02  01 *   *   *     ( cd /tmp; /my/path/to/script; intelmqctl reload bot-id )

And replace bot-id with the ID of the bot using the updated data.
If you do not reload the bot, the old data is still used.

Or use the template in `intelmq-update-data` moving it to `/etc/cron.d/` and
adapting them as needed. Do not forget to reload the affected bots.

## Path

If your executables are in `/usr/bin/local/`, make sure this path is in the PATH of cron. You can add it by a line like this in your local crontab file:

```
PATH=/bin:/usr/bin:/usr/local/bin
```

Otherwise `intelmqctl` can't find the executables' paths and check if they are running correctly.
