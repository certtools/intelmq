# -*- coding: utf-8 -*-
"""
Request Tracker output bot

Creates a ticket in the specified queue
Parameters:
rt_uri, rt_user, rt_password, verify_cert -  RT API endpoint
queue - ticket destination queue
CF_mapping - mapping attributes-ticket CFs
final_status - what is final status for the created ticket
create_investigation - should we create Investigation ticket (in case of RTIR workflow)
fieldnames - attributes to include into investigation ticket
description_attr - which event attribute contains text message being sent to the recipient

"""

from intelmq.lib.bot import Bot
from intelmq.lib.exceptions import MissingDependencyError

try:
    import rt
except ImportError:
    rt = None


class RTOutputBot(Bot):

    def init(self):
        if rt is None:
            raise MissingDependencyError('rt', version='1.0.9')

        # Event attributes to be included in Investigation ticket communication
        self.fieldnames = getattr(self.parameters, 'investigation_fields')
        if isinstance(self.fieldnames, str):
            self.fieldnames = self.fieldnames.split(',')
        # Investigations ticket can be created only when we work with Incidents ticket
        # and there is a parameter create_investigation provided
        if getattr(self.parameters, 'queue', 'None') == 'Incidents' and getattr(self.parameters, 'create_investigation', False):
            self.create_investigation = True
        else:
            self.create_investigation = False
        self.final_status = getattr(self.parameters, 'final_status', None)
        self.CF_mapping = getattr(self.parameters, 'CF_mapping', None)
        self.verify_cert = getattr(self.parameters, 'verify_cert', True)
        self.uri = getattr(self.parameters, 'rt_uri', None)
        self.user = getattr(self.parameters, 'rt_user', None)
        self.password = getattr(self.parameters, 'rt_password', None)
        self.description_attr = getattr(self.parameters, 'description_attr', None)

    def process(self):
        event = self.receive_message()
        RT = rt.Rt(self.uri, verify_cert=self.verify_cert)
        if not RT.login(self.user,
                        self.password):
            raise ValueError('Login failed.')
        kwargs = {}
        # we make subject in form of "Incident notification, IP"
        self.subject = 'Incident notification'
        self.content = ''

        if event.get('source.ip'):
            self.subject += ", " + event['source.ip']
        if event.get(self.description_attr):
            self.content = event[self.description_attr] + "\n\n"

        ticket_content = self.content
        for key, value in event.items():
            # Add all event attributes to the body of the incident ticket
            ticket_content += key + ": " + str(value) + "\n"
            # Add some (mapped) event attributes to the Custom Fields of the ticket
            if self.CF_mapping.get(key):
                str_value = str(value)
                kwargs["CF_" + self.CF_mapping.get(key)] = str_value
                self.logger.debug("Added custom field CF_%s: %s", self.CF_mapping.get(key), kwargs["CF_" + self.CF_mapping.get(key)])
        self.logger.debug("RT ticket subject: %s", self.subject)
        ticket_id = RT.create_ticket(Queue=self.parameters.queue, Subject=self.subject, Text=ticket_content, **kwargs)
        if ticket_id > -1:
            self.logger.debug("RT ticket created: %i", ticket_id)
            if event.get('source.abuse_contact') and event.get(self.description_attr) and self.create_investigation:
                ticket_content = self.content
                requestor = event.get('source.abuse_contact')
                # only selected fields goes to the investigation
                for key in self.fieldnames:
                    if event.get(key):
                        ticket_content += key + ": " + str(event.get(key)) + "\n"
                # Creating Investigation ticket
                # Communication supposed to be done by RT On Create scrip
                investigation_id = RT.create_ticket(Queue="Investigations", Subject=self.subject, Text=ticket_content, Requestor=requestor)

                if investigation_id > -1:
                    self.logger.debug("Investigation ticket created: %i", investigation_id)
                    # make a link between Incident and Investigation tickets
                    if RT.edit_link(investigation_id, 'MemberOf', ticket_id):
                        self.logger.debug("Investigation ticket %i linked to parent: %i", investigation_id, ticket_id)
                    else:
                        self.logger.error("Failed to link tickets %i -> %i", ticket_id, investigation_id)
                else:
                    self.logger.error("Failed to create RT Investigation ticket")
            if self.final_status:
                if RT.edit_ticket(ticket_id, Status=self.final_status):
                    self.logger.debug("Status changed to %s for ticket %i", self.final_status, ticket_id)
                else:
                    self.logger.error("Failed to change status for RT ticket %i", ticket_id)
        else:
            self.logger.error("Failed to create RT ticket")
        self.acknowledge_message()


BOT = RTOutputBot
