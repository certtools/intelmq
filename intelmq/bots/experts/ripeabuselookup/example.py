#!/usr/bin/env python

'''
Reference: https://stat.ripe.net/data/abuse-contact-finder/data.json?resource=1.1.1.1

Be careful, sometimes there is no response when there is no abuse_c field in RIPE
FIXME: create cache! Lookups are sloooowwww....

'''


import json
import pprint
import requests

url = 'https://stat.ripe.net/data/abuse-contact-finder/data.json?resource=193.238.156.2'
data = ''
response = requests.get(url, data=data)

print (response.json()['data']['anti_abuse_contacts']['abuse_c'][0]['email'])


