import json
import requests

class RIPENCC():

    @staticmethod
    def query(ip):

	url = 'https://stat.ripe.net/data/abuse-contact-finder/data.json?resource=' + ip
	response = requests.get(url, data="")

        try:
            if (response.json()['data']['anti_abuse_contacts']['abuse_c']):
                return (response.json()['data']['anti_abuse_contacts']['abuse_c'][0]['email'])
            else:
                return None
        except:
            return None