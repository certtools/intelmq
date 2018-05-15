# -*- coding: utf-8 -*-
"""
domaintools expert: query domtaintools.com to get a reputation score for a domain name

"""
from intelmq.lib.bot import Bot
try:
    from domaintools import API, exceptions
except ImportError:
    API = None


class DomaintoolsExpertBot(Bot):

    def init(self):
        self.logger.info("Loading Domaintools expert.")

        if not API:
            raise ValueError("need to have the domaintools API installed. See https://github.com/domaintools/python_api.")

        if not self.parameters.user:
            raise ValueError("need to specify user for domaintools expert in runtime.conf.")

        if not self.parameters.password:
            raise ValueError("need to specify password for the user for domaintools expert in runtime.conf.")

        self.api = API(self.parameters.user, self.parameters.password)

        if not self.valid_credentials():
            raise ValueError("invalid credentials found in runtime.conf.")

    def valid_credentials(self):
        resp = self.api.reputation(fqdn, include_reasons=False)
        try:
            resp['risk_score']
            return True
        except exceptions.NotAuthorizedException:
            return False

    def get_score(self, fqdn):
        # don't include a reason in the JSON response
        resp = self.api.reputation(fqdn, include_reasons=False)

        try:
            score = resp['risk_score']
        except exceptions.NotFoundException:
            score = None
        except exceptions.BadRequestException:
            raise

        return score

    def process(self):
        event = self.receive_message()
        extra = {}

        for key in ["source.", "destination."]:
            key_fqdn = key + "fqdn"

            if key_fqdn not in event:
                continue
            
            score = self.get_score(event.get(key_fqdn))
            
            if score:
                extra["domaintools_score_" + key_fqdn] = score
        
        extra.update(event.get("extra"))
        event.update("extra", extra)

        self.send_message(event)
        self.acknowledge_message()


BOT = DomaintoolsExpertBot
