# intelmq stomp output

This collector will push data to any STOMP stream.
STOMP stands for Streaming Text Oriented Messaging Protocol. See: https://en.wikipedia.org/wiki/Streaming_Text_Oriented_Messaging_Protocol


For the sake of explanations, we will use the N6 (n6.cert.pl) server as an example.

# Installation

  1. Install the stomp.py library from pip: `# pip install stomp.py`
  2. First please check if the CA certificate in this repository is still current for n6steam.cert.pl. If not, let us know.
  3. You will need a client certificate from the organization / server you are connecting to. Also you will need a so called "exchange point".
     In our example (n6.cert.pl) , you need to request a client certificate from CERT.pl: http://n6.cert.pl/jak.php. 
  4. save the client certificate in a suitable location (for example `/opt/intelmq/etc/client.pem`,  `/opt/intelmq/etc/client.key`)
  5. Edit your `runtime.conf` and add the location of your client certificates & key and the CA certificate. Also set the exchange point in 
     your runtime.conf.
  6. test your system:

```
% sudo -Eu intelmq python -m intelmq.bots.outputs.stomp.output stomp-output
on_connecting n6stream.cert.pl 61614
on_send STOMP {'accept-version': '1.1', 'heart-beat': '60000,60000'}
on_connected {'session': 'session-$randomstring', 'version': '1.1', 'server': 'RabbitMQ/3.5.4', 'heart-beat': '60000,60000'}
```

Please confirm with your STOMP connection partner that he/she receives your STOMP frames (messages).

NOTE: this bot does **NOT** do any re-formatting, transcoding, mapping of formats etc. It sends plain intelmq messages via the STOMP protocol
inside the body content.



