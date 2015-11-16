# intelmq n6stomp collector

This collector will fetch data from CERT Polska's n6 STOMP stream.
See also http://n6.cert.pl/
(might have to use google translate)


# Installation

  1. First please check if the CA certificate in this repository is still current for n6steam.cert.pl. If not, let us know.
  2. Second, request a client certificate from CERT.pl: http://n6.cert.pl/jak.php. Also ask for the proper exchange point.
  3. save the client certificate in a suitable location (for example `/opt/intelmq/etc/n6clientcert.pem`,  `/opt/intelmq/etc/n6clientcert.key`)
  4. Edit your `runtime.conf` and add the location of your client certificates & key and the CA certificate. Also set the exchange point 
in your runtime.conf.
  5. test your system:
```
% sudo -Eu intelmq python -m intelmq.bots.collectors.n6.collector_stomp n6stomp-collector
on_connecting n6stream.cert.pl 61614
on_send STOMP {'accept-version': '1.1', 'heart-beat': '60000,60000'}
on_send SUBSCRIBE {'ack': u'auto', 'destination': u'/exchange/XXXXX/#', 'id': 1}
on_connected {'session': 'session-$randomstring', 'version': '1.1', 'server': 'RabbitMQ/3.5.4', 'heart-beat': '60000,60000'}

```
And watch some data coming in.






