# -*- coding: utf-8 -*-
"""Microsoft Defender API comment output bot

Adds a comment to an alert in Microsoft Defender ATP.

Requires credentials as described in
https://docs.microsoft.com/en-us/microsoft-365/security/defender-endpoint/exposed-apis-create-app-webapp?view=o365-worldwide
for an app with permissions to at least Read all alerts and Run
advanced queries.

Defender wants to include quite a lot of information that doesn't fit
in IntelMQ's default harmonisation, so it abuses the "extra" namespace
to store its information.

The Defender alert ID is read from the event field
"extra.defender_id", which is filled in by the Defender parser.

The comment is read verbatim from the specified field.

SPDX-FileCopyrightText: 2021 Linköping University <https://liu.se/>
SPDX-License-Identifier: AGPL-3.0-or-later

Parameters:

api_region: string, default None, cloud region for API calls. Either
            None (for worldwide) or one of [ "us", "eu", "uk" ].

tenant_id: string, your Office 365 tenant ID.

client_id: string, the client ID you created for this application.

client_secret: string, the secret you created for this application.

comment_field: string, the field in the IntelMQ event containing the
               comment text to be added.
"""
from intelmq.lib.bot import Bot
from intelmq.lib.utils import create_request_session
from intelmq.lib.harmonization import DateTime
from intelmq.lib.exceptions import ConfigurationError, MissingDependencyError

try:
    from oauthlib.oauth2 import BackendApplicationClient
    from requests_oauthlib import OAuth2Session
except:
    BackendApplicationClient = None

import json
from typing import Optional


class DefenderCommentOutputBot(Bot):
    api_region: Optional[str] = None
    tenant_id: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    comment_field: Optional[str] = None

    def init(self):
        if BackendApplicationClient is None:
            raise MissingDependencyError("oauthlib-requests")

        if not self.tenant_id:
            raise ConfigurationError("API", "No tenant ID specified")

        if not self.client_id:
            raise ConfigurationError("API", "No client ID specified")

        if not self.client_secret:
            raise ConfigurationError("API", "No client secret specified")

        if not self.comment_field:
            raise ConfigurationError("Runtime", "No comment field specified")

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

    def update_alert(self, oauth, defender_id, comment):
        result = {}

        self.logger.info("Updating Defender alert %s with comment %s.", defender_id, comment)
        r = oauth.patch(self.api_uri + "/alerts/" + defender_id, data=json.dumps({"comment": comment}))
        self.logger.debug("Status: %s, text: %s.", r.status_code, r.text)
        try:
            result = json.loads(r.text)
            if "error" in result:
                self.logger.warning("Error adding comment to alert %s: %s.", defender_id, result["error"])
                result = {}
        except json.decoder.JSONDecodeError as e:
            self.logger.error("JSON error adding comment to alert: %s, Raw: %s.", str(e), r.text)
        except KeyError as e:
            self.logger.error("Error adding comment to alert: Key not found: %s, Raw: %s.", str(e), r.text)
        finally:
            return result

    def process(self):
        event = self.receive_message()

        client = BackendApplicationClient(client_id=self.client_id)
        oauth = OAuth2Session(client=client)
        oauth.fetch_token(token_url=self.token_uri, client_id=self.client_id, client_secret=self.client_secret,
                          body=f"resource={self.resource_uri}")

        defender_id = event.get("extra.defender_id", None)
        comment = event.get(self.comment_field, None)
        if not defender_id:
            self.logger.error("Event did not contain a Defender ID: %s.", event)
        elif not comment:
            self.logger.error("Event did not contain a comment: %s.", event)
        else:
            self.update_alert(oauth, defender_id, comment)

        self.acknowledge_message()


BOT = DefenderCommentOutputBot
