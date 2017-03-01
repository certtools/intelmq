# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from intelmq.lib.bot import Bot
import sys
from intelmq.lib.cache import Cache
from intelmq.lib.message import Event
import logging
import os
import ast


class MailGatherOutputBot(Bot):
    
    def init(self):
        self.cache = Cache(
                            self.parameters.redis_cache_host,
                            self.parameters.redis_cache_port,
                            self.parameters.redis_cache_db,
                            self.parameters.redis_cache_ttl
                          )
        self.logger.warning("Bot init succesful.")


    def process(self):
        message = self.receive_message()
        mail_rewrite = ast.literal_eval(self.parameters.mail_rewrite)

        self.logger.warning("ZPRAVA..")
        self.logger.debug(message)
        
        #message.add("source.abuse_contact",u"edvard.rejthar+test_abusemail@nic.cz") # XXX nevim, zda nepouzit https://github.com/certtools/intelmq/blob/master/docs/Harmonization-fields.md treba destination.account, nebo source.account
        self.logger.warning("ZPRAVA END..")
        if "source.abuse_contact" in message:
            field = message["source.abuse_contact"]
            self.logger.warning("mail:"+field)
            if field:
                self.logger.warning("edvard field")
                mails = field if type(field) == 'list' else [field]
            for mail in mails:
                self.logger.warning("edvard mails")

                # rewrite destination address
                if message["source.abuse_contact"] in mail_rewrite:
                    message.update("source.abuse_contact",
                                   str(mail_rewrite[message["source.abuse_contact"]]))
                    mail = mail_rewrite[mail]

                self.cache.redis.rpush("mail:"+mail, message)
            self.logger.warning("done")

        #self.send_message(message) nikam dal neposilame
        self.acknowledge_message() # dokoncil jsem praci (asi)


BOT = MailGatherOutputBot    
