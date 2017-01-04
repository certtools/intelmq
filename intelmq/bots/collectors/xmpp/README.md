# XMPP - Collector

The XMPP Collector is capable of collecting Messages from XMPP rooms and direct messages.

## Requirements
The Sleekxmpp - Library needs to be installed on your System 

## Parameters

 - `xmpp_user` : The username of the XMPP-Account the collector shall use (part before the @ sign)
 - `xmpp_server` : The domainname of the Server of the XMPP-Account (part after the @ sign)
 - `xmpp_password` : The password of the XMPP-Account
 - `xmpp_room` : The room which which has to be joined by the XMPP-Collector (full address room@conference.server.tld) 
 - `xmpp_room_nick` : The username / nickname the collector shall use within the room.
 - `xmpp_room_password` : The password which might be required to join a room
 - `use_muc` : If this parameter is `true`, the bot will join the room `xmpp_room`.
 - `ca_certs` : A path to a file containing the CA's which should be used
 - `xmpp_userlist`: An array of usernames whose messages will (not) be processed.
 - `xmpp_whitelists_mode`: If `true` the the list provided in `xmpp_process` is a whitelist. Else it is a blacklist.
    In case of a whitelist, only messages from the configured users will be processed, else their messages are not
    processed. Default ist `false` / blacklist.

