"""Choose the most relevant contacts
"""

from intelmq.bots.experts.certbund_contact.rulesupport \
    import keep_most_specific_contacts


def determine_directives(context):
    keep_most_specific_contacts(context)
