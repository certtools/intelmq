Bots documentation
==================

Experts
-------

| name | IPv6 | lookup | public | cache: redis db | information | comment |
|:-----|:-----|:---------|:--------|
| abusix | n | ? | y | 5 | ip to abuse contact | ipv6 implementation missing |
| asn-lookup | n | local db | y | - | ip to asn | [IPv6 bugreport](https://github.com/hadiasghari/pyasn/issues/14)
| certat-contact | n | https | y | - | asn to cert abuse contact, cc |
| cymru-whois | y | cymru dns | y | 6 | ip to geolocation, asn, network |
| deduplicator | y | redis cache | y | 7 | - | not tested |
| filter | y | - | y | - | drops event | not tested |
| maxmind-geoip | ? | local db | n | - | ip to geolocation ? | not stable |
| reverse-dns | n | dns | y | 8 | ip to domain | ipv6 implementation missing |
| ripencc-abuse-contact | y | ? | y | 9 | ip to abuse contact |
| taxonomy | - | - | y | - | classification type to taxonomy |
| tor-nodes | n | local db | y | - | if ip is tor node |
