"""Handle inhibition annotations

This script handles inhibition annotations. This script never generates
any notifications itself, but it tells the rule expert bot not to
process any further scripts (by having determine_directives return True)
if the condition of any annotation associated with the event matches the
event.

Most of the actual work is done by :py:func:`notification_inhibited`.
See its documentation for details.
"""

from intelmq.bots.experts.certbund_contact.rulesupport \
    import notification_inhibited

"""
This list of Tags defines Tag-names and conditions when a tag matches.
The concept is quite similar to inhibitions, but moves the configuration
efforts to another place. In this case the high efforts are on the skripting
side and not on the Contact-DB side.

When using inhibitions, the complex configuration has to be done on the
contactdb side.
"""
WHITELIST_TAGS = {
    "whitelist-malware": {
        "field": "classification.type",
        "values": ["botnet drone"]
    },
    "whitelist-opendns": {
        "field": "classification.identifier",
        "values": ["opendns"]
    }
}


def determine_directives(context):
    if notification_inhibited(context):
        # According to annotations, no notifications should be sent.
        # Assuming this script is run before any notification directives
        # are added to the context, we can simply return True to
        # indicate that no more rules should be processed to inhibit all
        # notifications for this event.
        return True
    if inhibited_by_tag(context):
        # According to the Tags of the Organisation or Network
        # This event should not be reported.
        return True


def inhibited_by_tag(context):
    """
    Compare the annotations with the dict above.
    Check if the field "field" contains one of
    the values in "values"
    """
    annotations = context.all_annotations()
    tags = set()
    for a in annotations:
        if a.tag != "inhibition":
            tags.add(a.tag)

    for t in tags.intersection(WHITELIST_TAGS):
        field = WHITELIST_TAGS[t]["field"]
        values = WHITELIST_TAGS[t]["values"]
        if context.get(field) in values:
            return True

    return False
