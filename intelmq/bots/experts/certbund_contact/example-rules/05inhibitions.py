"""Handle inhibitions
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
