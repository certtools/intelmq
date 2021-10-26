# -*- coding: utf-8 -*-
"""Microsoft Defender API collector bot

Fetches security alerts from Microsoft Defender ATP.

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

lookback: integer, default rate_limit, get events for the last this
          many seconds on every run. Setting this higher than
          rate_limit will yield duplicate events in the overlapping
          time slice, and setting it lower will lose events between
          runs.

rate_limit: integer, default 60, number of seconds to sleep between
            runs. Must be >= 2, since the API defaults to throttling
            clients connecting more than 100 times/minute.
"""
from intelmq.lib.bot import CollectorBot
from intelmq.lib.exceptions import ConfigurationError, MissingDependencyError

try:
    from oauthlib.oauth2 import BackendApplicationClient
    from requests_oauthlib import OAuth2Session
except:
    BackendApplicationClient = None

from datetime import datetime, timezone, timedelta
import json
from typing import Optional


class DefenderCollectorBot(CollectorBot):
    api_region: Optional[str] = None
    tenant_id: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    lookback: int = 0
    rate_limit: int = 60

    def init(self):
        if BackendApplicationClient is None:
            raise MissingDependencyError("oauthlib-requests")

        if not self.tenant_id:
            raise ConfigurationError("API", "No tenant ID specified")

        if not self.client_id:
            raise ConfigurationError("API", "No client ID specified")

        if not self.client_secret:
            raise ConfigurationError("API", "No client secret specified")

        if self.rate_limit < 2:
            raise ConfigurationError("Runtime", "rate_limit must be >= 2 seconds to avoid throttling")

        if self.lookback == 0:
            self.lookback = self.rate_limit

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
        self.alert_path = "/alerts"

    def process(self):
        client = BackendApplicationClient(client_id=self.client_id)
        oauth = OAuth2Session(client=client)
        oauth.fetch_token(token_url=self.token_uri, client_id=self.client_id, client_secret=self.client_secret,
                          body=f"resource={self.resource_uri}")

        dt = datetime.now(tz=timezone.utc) - timedelta(seconds=self.lookback)
        date_string = dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")  # 2021-04-05T12:55:39.9213313Z
        time_filter = f"?$filter=alertCreationTime ge {date_string}"
        options = "&$expand=evidence"

        self.logger.debug("Fetching alerts: %s.", self.api_uri + self.alert_path + time_filter + options)
        r = oauth.get(self.api_uri + self.alert_path + time_filter + options)

        try:
            response = json.loads(r.text)
        except json.decoder.JSONDecodeError as e:
            self.logger.error("Error: %s, Raw: %s.", str(e), r.text)
            return

        if "error" in response:
            self.logger.error("API error: %s.", response['error'])
            return

        if "value" in response:
            alerts = response["value"]
        else:
            self.logger.error("API response did not contain 'value'. Response: %s.", r.text)
            return

        for alert in alerts:
            self.logger.debug("Fetched alert: %s.", alert)
            report = self.new_report()
            report.add("feed.url", self.api_uri)
            report.add("raw", json.dumps(alert))
            self.send_message(report)


BOT = DefenderCollectorBot
