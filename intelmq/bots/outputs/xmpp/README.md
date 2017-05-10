# XMPP - Output

The XMPP Output is capable of sending Messages to XMPP Rooms and as direct messages.

## Requirements
The Sleekxmpp - Library needs to be installed on your System

## Parameters

 - `xmpp_user` : The username of the XMPP-Account the output shall use (part before the @ sign)
 - `xmpp_server` : The domain name of the server of the XMPP-Account (part after the @ sign)
 - `xmpp_password` : The password of the XMPP-Account
 - `xmpp_to_user` : The username of the receiver
 - `xmpp_to_server` : The domain name of the receiver
 - `xmpp_room` : The room which which has to be joined by the output (full address a@conference.b.com)
 - `xmpp_room_nick` : The username / nickname the output shall use within the room.
 - `xmpp_room_password` : The password which might be required to join a room
 - `use_muc` : If this parameter is `true`, the bot will join the room `xmpp_room`.
 - `ca_certs` : A path to a file containing the CA's which should be used
