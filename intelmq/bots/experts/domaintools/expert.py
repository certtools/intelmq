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
        if (not API):
            self.logger.exception("need to have the domaintools API installed. See https://github.com/domaintools/python_api")
            self.stop()
        if (not self.parameters.user):
            self.logger.exception("need to specify user for domaintools expert in runtime.conf. Exiting")
            self.stop()
        if (not self.parameters.password):
            self.logger.exception("need to specify password for the user for domaintools expert in runtime.conf. Exiting")
            self.stop()
        self.api = API(self.parameters.user, self.parameters.password)

    def domaintools_get_score(self, fqdn):
        score = None
        if fqdn:
            resp = self.api.reputation(fqdn, include_reasons=False)     # don't include a reason in the JSON response

            try:
                score = resp['risk_score']
            except exceptions.NotFoundException:
                score = None
            except exceptions.BadRequestException:
                score = None
            return score

    def process(self):
        event = self.receive_message()
        extra = {}

        for key in ["source.", "destination."]:
            key_fqdn = key + "fqdn"
            if key_fqdn not in event:
                continue        # can't query if we don't have a domain name
            score = self.domaintools_get_score(event.get(key_fqdn))
            if score is not None:
                extra["domaintools_score"] = score
                event.add("extra", extra)

        self.send_message(event)
        self.acknowledge_message()


BOT = DomaintoolsExpertBot
