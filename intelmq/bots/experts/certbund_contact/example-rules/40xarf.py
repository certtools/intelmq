"""Sample notification rules for Organisation Annotations.

If an Organisation carries the tag "xarf" all a
directive is created for all contacts associated to this organisation
which states the explicit wish to notify the contact in x-arf format.

"""

from intelmq.bots.experts.certbund_contact.rulesupport import Directive


# default X-ARF settings
xarf_settings = Directive(template_name="generic-xarf-description.txt",
                          notification_format="xarf",
                          event_data_format="bot-infection_0.2.0_unstable",
                          notification_interval=0)


def determine_directives(context):
    if context.section == "destination":
        return

    directive_set = False
    for org in context.organisations:
        if any(annotation.tag == "xarf" for annotation in org.annotations):
            context.logger.debug("Create X-ARF Directive")
            context.logger.debug(org.contacts)
            for contact in org.contacts:
                directive = Directive.from_contact(contact)
                directive.update(xarf_settings)
                context.add_directive(directive)
                directive_set = True
    return directive_set
