"""Only handle those organisations which are participating
in the test-run. Currently those are all Orgs that were
added manually.
"""

def determine_directives(context):
    context.logger.debug("============= 06testbetrieb.py ===========")
    context.logger.debug("Content of the Context BEFORE this script:")
    context.logger.debug("Organisations %r" % context.organisations)
    context.logger.debug("Matches %r" % context.matches)


    # Determine all manual matches, and the IDs of the Organisations
    # associated to this match.

    matching_orgs_manual = set()
    new_matches = []

    for match in context.matches:
        # Only take the manual datasets
        if match.managed == 'manual':
            # Add this match to "new_matches"
            new_matches.append(match)
            # and write the ID of this matches organisation to the array.
            for org in match.organisations:
                matching_orgs_manual.append(org)


    # Now we know the IDs of the organisations which were added manually.
    # As all manual matches were written into the new_matches list, we can
    # overwrite the context's matches list with the new list.
    # This would already suffice to stop notifying automatic contacts.
    # But we want to be a bit more tidy, so we are removing the orgs, too.

    new_orgs = []
    for m in matching_orgs_manual:
        org = context.lookup_organisation(m)
        new_orgs.append(org)

    # Overwrite the context 
    context.matches = new_matches
    context.organisations = new_orgs
    
    context.logger.debug("Content of the Context AFTER this script:")
    context.logger.debug("Organisations %r" % context.organisations)
    context.logger.debug("Matches %r" % context.matches)
    
    # We'll return None, as other scripts shall still run....
    return None 
