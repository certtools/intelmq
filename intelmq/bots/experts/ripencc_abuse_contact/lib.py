# -*- coding: utf-8 -*-
import requests

URL_STAT = ('https://stat.ripe.net/data/abuse-contact-finder/'
            'data.json?resource={}')
URL_DB_IP = 'http://rest.db.ripe.net/abuse-contact/{}.json'
URL_DB_AS = 'http://rest.db.ripe.net/abuse-contact/as{}.json'


def query_ripestat(resource):
    response = requests.get(URL_STAT.format(resource), data="")
    if response.status_code != 200:
        raise ValueError('HTTP response status code was {}.'
                         ''.format(response.status_code))

    try:
        if (response.json()['data']['anti_abuse_contacts']['abuse_c']):
            return [response.json()['data']['anti_abuse_contacts']
                    ['abuse_c'][0]['email']]
        else:
            return []
    except:
        return []


def query_ripedb(ip=None, asn=None):
    response = requests.get(URL_DB_IP.format(ip), data="")
    if response.status_code != 200:
        return []

    return [response.json()['abuse-contacts']['email']]


def query_asn(asn):
    response = requests.get(URL_DB_AS.format(asn), data="")
    if response.status_code != 200:
        return []

    return [response.json()['abuse-contacts']['email']]
