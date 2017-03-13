"""Sample notification rules for Organisation Annotations.

If an Organisation carries the tag "xarf" all a
directive is created for all contacts associated to this organisation
which states the explicit wish to notify the contact in x-arf format.

"""

from intelmq.bots.experts.certbund_contact.rulesupport import Directive


def determine_directives(context):
    if context.section == "destination":
        return

    orglist = context.organisations
    if orglist:
        for org in orglist:
            sendXarf = False
            for an in org.annotations:
                if an.tag == "xarf":
                    context.logger.debug("Setting sendXarf")
                    sendXarf = True
            if sendXarf:
                context.logger.debug("Create X-ARF Directive")
                context.logger.debug(org.contacts)
                for contact in org.contacts:
                    directive = Directive.from_contact(contact)
                    directive.update(xarf_entry())
                    context.add_directive(directive)
                    context.logger.debug(directive)
                return True
    return


def xarf_entry():
    return Directive(template_name="bot-infection_0.2.0_unstable",
                     event_data_format="xarf",
                     notification_interval=0)