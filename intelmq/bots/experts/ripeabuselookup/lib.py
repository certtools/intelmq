#!/usr/bin/env python


import json
import requests

class RIPENCC():

    @staticmethod
    def query(ip, ip_version):
	url = 'https://stat.ripe.net/data/abuse-contact-finder/data.json?resource=' + ip
	data = ''
	response = requests.get(url, data=data)
	try:
		if (response.json()['data']['anti_abuse_contacts']['abuse_c']):
			return (response.json()['data']['anti_abuse_contacts']['abuse_c'][0]['email'])
		else:
			return None
	except:	# catchall
		print "no abuse contact for ip: " + ip
		return None


