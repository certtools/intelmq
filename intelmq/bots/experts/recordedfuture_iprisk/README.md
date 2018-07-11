This Bot tags events with score found in recorded futures large IP risklist.

The list is obtained from recorded future API and needs a valid API TOKEN
The large list contains all IP's with a risk score of 25 or more.
If IP's are not present in the database a risk score of 0 is given


A script is supplied that may be run as intelmq to update the database.
The script needs to be edited to use a valid API token.

Download database:

```bash
mkdir /opt/intelmq/var/lib/bots/recordedfuture_iprisk
cd /tmp/
curl -H "X-RFToken: [API Token]" --output rfiprisk.dat.gz "https://api.recordedfuture.com/v2/ip/risklist?format=csv%2Fsplunk&gzip=true&list=large"
bunzip rfiprisk.dat.gz
mv rfiprisk.dat /opt/intelmq/var/lib/bots/recordedfuture_iprisk/rfiprisk.dat
chown intelmq.intelmq -R /opt/intelmq/var/lib/bots/recordedfuture_iprisk
```

Configure 'runtime.conf' with the following parameter:

    "database": "/opt/intelmq/var/lib/bots/recordedfuture_iprisk/rfiprisk.dat"
