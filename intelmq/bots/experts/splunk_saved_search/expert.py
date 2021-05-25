# -*- coding: utf-8 -*-
"""Splunk saved search enrichment export bot

SPDX-FileCopyrightText: 2020 Linköping University <https://liu.se/>
SPDX-License-Identifier: AGPL-3.0-or-later

Searches Splunk for fields in an event and adds search results to it.

This bot is quite slow, since it needs to submit a search job to
Splunk, get the job ID, poll for the job to complete and then retrieve
the results. If you have a high query load, run more instances of the
bot.

Parameters:

    Generic IntelMQ HTTP parameters

    auth_token: string, Splunk authentication token

    url: string, base URL of the Splunk REST API

    retry_interval: integer, optional, default 5, number of seconds to
                    wait between polling for search results to be
                    available

    saved_search: string, name of Splunk saved search to run

    search_parameters: map string->string, optional, default {},
                       IntelMQ event fields to Splunk saved search
                       parameters

    result_fields: map string->string, optional, default {}, Splunk
                   search result fields to IntelMQ event fields

    not_found: list of strings, default [ "warn", "send" ], what to do
               if the search returns zero results. All specified
               actions are performed. Any reasonable combination of:
               warn: log a warning message
               send: send the event on unmodified
               drop: drop the message

    multiple_result_handling: list of strings, default [ "warn",
                              "use_first", "send" ], what to do if the
                              search returns more than one result. All
                              specified actions are performed. Any
                              reasonable combination of:
                              limit: limit the search so that duplicates
                                     are impossible
                              warn: log a warning message
                              use_first: use the first search result
                              ignore: do not modify the event
                              send: send the event on
                              drop: drop the message

    overwrite: bool or null, optional, default null, whether search
               results replace existing values in the event. If null,
               trying to set an existing field raises
               intelmq.exceptions.KeyExists.

"""

try:
    import requests
except ImportError:
    requests = None

import intelmq.lib.utils as utils
from intelmq.lib.bot import Bot
from intelmq.lib.exceptions import MissingDependencyError, ConfigurationError
import time


class SplunkSavedSearchBot(Bot):
    """Enrich an event from Splunk search results"""
    auth_token: str = None
    multiple_result_handling = ["warn", "use_first", "send"]
    not_found = ["warn", "send"]
    overwrite = None
    result_fields = {"result field": "event field"}
    retry_interval: int = 5
    saved_search: str = None
    search_parameters = {"event field": "search parameter"}
    url: str = None

    __is_multithreadable = False

    def init(self):
        if requests is None:
            raise MissingDependencyError("requests")

        if self.url is None:
            raise ConfigurationError("Connection", "No Splunk API URL specified")
        if self.auth_token is None:
            raise ConfigurationError("Connection", "No Splunk API authorization token specified")
        if self.saved_search is None:
            raise ConfigurationError("Search", "No Splunk saved search specified")

        if "send" in self.not_found and "drop" in self.not_found:
            raise ConfigurationError("Processing", "Cannot both drop and send messages without search results")

        if "limit" in self.multiple_result_handling and len(self.multiple_result_handling) != 1:
            raise ConfigurationError("Processing", "Search results limited to one, no processing of multiple results possible")
        if "send" in self.multiple_result_handling and "drop" in self.multiple_result_handling:
            raise ConfigurationError("Processing", "Cannot both drop and send messages with multiple search results")
        if "ignore" in self.multiple_result_handling and "use_first" in self.multiple_result_handling:
            raise ConfigurationError("Processing", "Cannot both ignore and use multiple search results")

        self.set_request_parameters()

        self.http_header.update({"Authorization": "Bearer {}".format(self.auth_token)})

        self.session = utils.create_request_session(self)
        self.session.keep_alive = False

    def update_event(self, event, search_result):
        self.logger.info("Updating event: %s",
                         dict([(field, search_result[field]) for field in self.result_fields]))
        for result, field in self.result_fields.items():
            event.add(field, search_result[result], overwrite=self.overwrite)

    def process(self):
        event = self.receive_message()

        for field, parameter in self.search_parameters.items():
            if field not in event:
                self.logger.warning("Event %s does not contain search parameter %s", event, field)
                self.send_message(event)
                self.acknowledge_message()
                return

        self.logger.debug("Received event, searching for %s",
                          dict([(parameter, event[field]) for field, parameter in self.search_parameters.items()]))

        query = '|savedsearch "{saved_search}"'.format(saved_search=self.saved_search)
        for field, parameter in self.search_parameters.items():
            query += ' "{parameter}"="{field}"'.format(parameter=parameter, field=event[field])
        if "limit" in self.multiple_result_handling:
            query += " | head 1"

        self.logger.debug("Query: %s", query)

        req = self.session.post(url=self.url + "/services/search/jobs",
                                data={"output_mode": "json", "search": query},
                                timeout=self.http_timeout_sec)

        if not req.ok:
            self.logger.error("Error starting search job: %r",
                              req.text)
            req.raise_for_status()

        jobid = req.json()['sid']

        self.logger.debug("Started search, job id: %i", jobid)

        # Even the simplest search is never ready immediately, so to
        # avoid polling and waiting a full retry_interval for every
        # search, sleep briefly here in the hope that a simple search
        # will be ready afterwards.
        time.sleep(1)

        results_ready = False
        while not results_ready:
            req = self.session.get(url=self.url +
                                   "/services/search/jobs/" + jobid + "/results/",
                                   data={"output_mode": "json"},
                                   timeout=self.http_timeout_sec)

            if req.status_code == 200:
                results_ready = True
            elif req.status_code == 204:
                results_ready = False
                self.logger.debug("Results not ready, sleeping for %s seconds before retrying", self.retry_interval)
                time.sleep(self.retry_interval)
            else:
                self.logger.error("Error getting search results: %s", req.text)
                req.raise_for_status()

        hits = req.json()['results']
        if len(hits) == 0:
            if "warn" in self.not_found:
                self.logger.warning("No results returned")
            if "drop" in self.not_found:
                self.logger.debug("Dropping message")
                self.acknowledge_message()
            if "send" in self.not_found:
                self.send_message(event)
                self.acknowledge_message()
        elif len(hits) > 1:
            if "warn" in self.multiple_result_handling:
                self.logger.warning("Multiple results returned: %s", hits)
            if "use_first" in self.multiple_result_handling:
                self.logger.debug("Using first search result")
                self.update_event(event, hits[0])
            if "ignore" in self.multiple_result_handling:
                self.logger.debug("Ignoring search results")
            if "drop" in self.multiple_result_handling:
                self.logger.debug("Dropping message")
                self.acknowledge_message()
            if "send" in self.multiple_result_handling:
                self.send_message(event)
                self.acknowledge_message()
        else:
            self.update_event(event, hits[0])
            self.send_message(event)
            self.acknowledge_message()


BOT = SplunkSavedSearchBot
