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


def determine_directives(context):
    if notification_inhibited(context):
        # According to annotations, no notifications should be sent.
        # Assuming this script is run before any notification directives
        # are added to the context, we can simply return True to
        # indicate that no more rules should be processed to inhibit all
        # notifications for this event.
        return True
