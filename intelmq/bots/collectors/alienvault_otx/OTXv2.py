#!/usr/bin/env python

import json
import logging

from .IndicatorTypes import all_types, to_name_list

API_V1_ROOT = "{}/api/v1/"
PULSES_ROOT = "{}/pulses".format(API_V1_ROOT)
SUBSCRIBED = "{}/subscribed".format(PULSES_ROOT)
EVENTS = "{}/events".format(PULSES_ROOT)

try:
    # For Python2
    from urllib2 import URLError, HTTPError, build_opener, ProxyHandler
except ImportError:
    # For Python3
    from urllib.error import URLError, HTTPError
    from urllib.request import build_opener, ProxyHandler

logger = logging.getLogger("OTXv2")


class InvalidAPIKey(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class BadRequest(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class OTXv2(object):
    """
    Main class to interact with the AlienVault OTX API.
    """

    def __init__(self, api_key, proxy=None, server="https://otx.alienvault.com", project="SDK"):
        self.key = api_key
        self.server = server
        self.proxy = proxy
        self.sdk = 'OTX Python {}/1.0'.format(project)

    def get(self, url):
        """
        Internal API for GET request on a OTX URL
        :param url: URL to retrieve
        :return: response in JSON object form
        """
        if self.proxy:
            proxy = ProxyHandler({'http': self.proxy})
            request = build_opener(proxy)
        else:
            request = build_opener()
        request.addheaders = [
            ('X-OTX-API-KEY', self.key),
            ('User-Agent', self.sdk)
        ]
        response = None
        try:
            response = request.open(url)
        except URLError as e:
            if isinstance(e, HTTPError):
                if e.code == 403:
                    raise InvalidAPIKey("Invalid API Key")
                elif e.code == 400:
                    raise BadRequest("Bad Request")
            else:
                raise e
        data = response.read().decode('utf-8')
        json_data = json.loads(data)
        return json_data

    def create_url(self, url_path, **kwargs):
        uri = url_path.format(self.server)
        uri += "?"
        for parameter, value in kwargs.items():
            uri += parameter
            uri += "="
            uri += str(value)
            uri += "&"
        return uri

    def getall(self, limit=20):
        """
        Get all pulses user is subscribed to.
        :param limit: The page size to retrieve in a single request
        :return: the consolidated set of pulses for the user
        """
        pulses = []
        next = self.create_url(SUBSCRIBED, limit=limit)
        while next:
            json_data = self.get(next)
            for r in json_data["results"]:
                pulses.append(r)
            next = json_data["next"]
        return pulses

    def getall_iter(self, limit=20):
        """
        :param limit:
        :return:
        """
        pulses = []
        next = self.create_url(SUBSCRIBED, limit=limit)
        while next:
            json_data = self.get(next)
            for r in json_data["results"]:
                yield r
            next = json_data["next"]

    def getsince(self, mytimestamp, limit=20):
        """
        Get all pulses created or updated since a timestamp
        :param mytimestamp: timestamp to filter returned pulses
        :param limit: The page size to retrieve in a single request
        :return: the consolidated set of pulses for the user
        """
        pulses = []
        next = self.create_url(SUBSCRIBED, limit=limit, modified_since=mytimestamp)
        while next:
            json_data = self.get(next)
            for r in json_data["results"]:
                pulses.append(r)
            next = json_data["next"]
        return pulses

    def getsince_iter(self, mytimestamp, limit=20):
        pulses = []
        next = self.create_url(SUBSCRIBED, limit=limit, modified_since=mytimestamp)
        while next:
            json_data = self.get(next)
            for r in json_data["results"]:
                yield r
            next = json_data["next"]

    def get_all_indicators(self, indicator_types=all_types):
        """
        Get all the indicators contained within your pulses of the IndicatorTypes passed.
        By default returns all IndicatorTypes.
        :param indicator_types: IndicatorTypes to return
        :return: yields the indicator object for use
        """
        name_list = to_name_list(indicator_types)
        for pulse in self.getall_iter():
            for indicator in pulse["indicators"]:
                if indicator["type"] in name_list:
                    yield indicator

    def getevents_since(self, mytimestamp, limit=20):
        """
        Get all events (activity) created or updated since a timestamp
        :param mytimestamp: timestamp to filter returned activity
        :param limit: The page size to retrieve in a single request
        :return: the consolidated set of pulses for the user
        """
        events = []
        next = self.create_url(EVENTS, limit=limit, since=mytimestamp)
        while next:
            json_data = self.get(next)
            for r in json_data["results"]:
                events.append(r)
            next = json_data["next"]
        return events
