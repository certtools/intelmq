Download database (IPv4 and IPv6):

```bash
mkdir /opt/intelmq/var/lib/bots/tor_nodes
cd /tmp/
wget https://internet2.us/static/latest.bz2
bunzip latest.bz2
mv latest /opt/intelmq/var/lib/bots/tor_nodes/tor_nodes.dat
chown intelmq.intelmq -R /opt/intelmq/var/lib/bots/tor_nodes
```

Configure 'runtime.conf' with the following parameter:

    "database": "/opt/intelmq/var/lib/bots/tor_nodes/tor_nodes.dat"
