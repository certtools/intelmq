# -*- coding: utf-8 -*-
"""Microsoft Defender API advanced hunting expert bot

Fetches information by running queries against the Microsoft Defender
ATP advanced hunting API.

Requires credentials as described in
https://docs.microsoft.com/en-us/microsoft-365/security/defender-endpoint/exposed-apis-create-app-webapp?view=o365-worldwide
for an app with permissions to at least Read all alerts and Run
advanced queries.

SPDX-FileCopyrightText: 2021 Linköping University <https://liu.se/>
SPDX-License-Identifier: AGPL-3.0-or-later

Parameters:

api_region: string, default None, cloud region for API calls. Either
            None (for worldwide) or one of [ "us", "eu", "uk" ].

tenant_id: string, your Office 365 tenant ID.

client_id: string, the client ID you created for this application.

client_secret: string, the secret you created for this application.

query: string, the query to run, in Jinja2 format with the incoming
       event supplied as the variable named "event". E.g.:
         query: DeviceEvents | where DeviceId == "{{ event["extra.machineid"] }}" and ActionType == "AntivirusDetection"

result_fields: map string->string, optional, default {}, query result
               fields to IntelMQ event fields. E.g.:
               { "InitiatingProcessAccountName": "source.account" }

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
from intelmq.lib.bot import Bot
from intelmq.lib.exceptions import ConfigurationError, MissingDependencyError

try:
    from oauthlib.oauth2 import BackendApplicationClient
    from requests_oauthlib import OAuth2Session
except:
    BackendApplicationClient = None

import json
from typing import Optional, List

try:
    from jinja2 import Template
except:
    Template = None


class DefenderAdvancedHuntingExpertBot(Bot):
    api_region: Optional[str] = None
    tenant_id: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    query: Optional[str] = None
    multiple_result_handling: List[str] = ["warn", "use_first", "send"]
    not_found: List[str] = ["warn", "send"]
    overwrite: Optional[bool] = None

    def init(self):
        if Template is None:
            raise MissingDependencyError("jinja2")

        if BackendApplicationClient is None:
            raise MissingDependencyError("oauthlib-requests")

        if not self.tenant_id:
            raise ConfigurationError("API", "No tenant ID specified")

        if not self.client_id:
            raise ConfigurationError("API", "No client ID specified")

        if not self.client_secret:
            raise ConfigurationError("API", "No client secret specified")

        if self.api_region is None:
            api_host = "api"
        elif self.api_region in ["eu", "uk", "us"]:
            api_host = "api-" + self.api_region
        else:
            raise ConfigurationError("API", f'Unknown API region "{self.api_region}", must be None, "eu", "uk", or "us".')

        self.token_uri = f'https://login.microsoftonline.com/{self.tenant_id}/oauth2/token'
        self.base_uri = "securitycenter.windows.com"
        self.resource_uri = f"https://api.{self.base_uri}"
        self.api_uri = f"https://{api_host}.{self.base_uri}/api"
        self.advanced_query_path = "/advancedqueries/run"

        if self.query is None:
            raise ConfigurationError("Search", "No query specified")

        self.query_template = Template(self.query)

        if "send" in self.not_found and "drop" in self.not_found:
            raise ConfigurationError("Processing", "Cannot both drop and send messages without search results")
        if "send" not in self.not_found and "drop" not in self.not_found:
            raise ConfigurationError("Processing", "Must either drop or send messages without search results")

        if "limit" in self.multiple_result_handling and len(self.multiple_result_handling) != 1:
            raise ConfigurationError("Processing", "Search results limited to one, no processing of multiple results possible")
        if "send" in self.multiple_result_handling and "drop" in self.multiple_result_handling:
            raise ConfigurationError("Processing", "Cannot both drop and send messages with multiple search results")
        if "send" not in self.multiple_result_handling and "drop" not in self.multiple_result_handling and "limit" not in self.multiple_result_handling:
            raise ConfigurationError("Processing", "Must either drop or send messages with multiple search results")
        if "ignore" in self.multiple_result_handling and "use_first" in self.multiple_result_handling:
            raise ConfigurationError("Processing", "Cannot both ignore and use multiple search results")

    def run_advancedhunting(self, query):
        result = []

        self.logger.debug("Running OAuth2 authentication.")
        client = BackendApplicationClient(client_id=self.client_id)
        oauth = OAuth2Session(client=client)
        oauth.fetch_token(token_url=self.token_uri, client_id=self.client_id, client_secret=self.client_secret,
                          body=f"resource={self.resource_uri}")

        self.logger.debug("Running advanced hunting query: %s.", json.dumps(query))
        r = oauth.post(self.api_uri + self.advanced_query_path, data=json.dumps({"Query": query}))
        self.logger.debug("Status: %s, text: %s.", r.status_code, r.text)
        try:
            data = json.loads(r.text)
            if data.get("Results", None):
                result = data["Results"]
        except json.decoder.JSONDecodeError as e:
            self.logger.error("JSON error running advanced hunting query: %s, Raw: %s.", str(e), r.text)
        except KeyError as e:
            self.logger.error("Error running advanced hunting query: Key not found: %s, Raw: %s.", str(e), r.text)
        finally:
            return result

    def update_event(self, event, search_result):
        self.logger.info("Updating event: %s.",
                         dict([(field, search_result[field]) for field in self.result_fields]))
        for result, field in self.result_fields.items():
            event.add(field, search_result[result], overwrite=self.overwrite)

    def process(self):
        event = self.receive_message()

        query = self.query_template.render(event=event)
        if "limit" in self.multiple_result_handling:
            query += " | limit 1"

        results = self.run_advancedhunting(query)

        if len(results) == 0:
            if "warn" in self.not_found:
                self.logger.warning("No results returned.")
            if "drop" in self.not_found:
                self.logger.debug("Dropping message.")
                self.acknowledge_message()
            if "send" in self.not_found:
                self.send_message(event)
                self.acknowledge_message()
        elif len(results) > 1:
            if "warn" in self.multiple_result_handling:
                self.logger.warning("Multiple results returned: %s.", results)
            if "use_first" in self.multiple_result_handling:
                self.logger.debug("Using first query result.")
                self.update_event(event, results[0])
            if "ignore" in self.multiple_result_handling:
                self.logger.debug("Ignoring query results.")
            if "drop" in self.multiple_result_handling:
                self.logger.debug("Dropping message.")
                self.acknowledge_message()
            if "send" in self.multiple_result_handling:
                self.send_message(event)
                self.acknowledge_message()
        else:
            self.update_event(event, results[0])
            self.send_message(event)
            self.acknowledge_message()


BOT = DefenderAdvancedHuntingExpertBot
