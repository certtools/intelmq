"""Choose the most relevant contacts
"""

from intelmq.bots.experts.certbund_contact.rulesupport import \
     most_specific_contacts


def determine_directives(context):
    context.contacts = most_specific_contacts(context.contacts)
